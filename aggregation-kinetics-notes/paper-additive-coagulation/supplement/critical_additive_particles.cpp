// Gillespie simulation: additive coagulation and rate-one equal fragmentation.
// Every initial particle has unit mass; pair rates are (x_i+x_j)/n.
// Build: g++ -O3 -std=c++17 critical_additive_particles.cpp -o /tmp/critical_particles
// Run: /tmp/critical_particles INITIAL_COUNT SEED
#include <algorithm>
#include <cmath>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <limits>
#include <random>
#include <stdexcept>
#include <string>
#include <vector>

using Real = long double;

static void require(bool condition, const char* message) {
    if (!condition) throw std::runtime_error(message);
}

class Particles {
    std::vector<Real> masses_;
    std::vector<Real> tree_;

    void add(std::size_t index, Real increment) {
        for (std::size_t j = index + 1; j < tree_.size(); j += j & -j)
            tree_[j] += increment;
    }

    void grow() {
        tree_.assign(2 * (tree_.size() - 1) + 1, 0);
        masses_.reserve(tree_.size() - 1);
        for (std::size_t i = 0; i < masses_.size(); ++i) add(i, masses_[i]);
    }

public:
    explicit Particles(std::size_t initial_capacity = 16)
        : tree_(std::max<std::size_t>(initial_capacity, 1) + 1, 0) {
        masses_.reserve(tree_.size() - 1);
    }

    std::size_t size() const { return masses_.size(); }
    const std::vector<Real>& masses() const { return masses_; }

    Real total() const {
        Real sum = 0;
        for (std::size_t j = masses_.size(); j > 0; j -= j & -j) sum += tree_[j];
        return sum;
    }

    void append(Real mass) {
        require(mass > 0 && std::isfinite(mass), "Nonpositive or nonfinite mass");
        if (masses_.size() + 1 == tree_.size()) grow();
        const auto index = masses_.size();
        masses_.push_back(mass);
        add(index, mass);
    }

    void replace(std::size_t index, Real mass) {
        require(index < size() && mass > 0 && std::isfinite(mass), "Invalid replacement");
        const Real change = mass - masses_[index];
        masses_[index] = mass;
        add(index, change);
    }

    void remove(std::size_t index) {
        require(index < size(), "Invalid removal");
        const auto last = size() - 1;
        if (index != last) replace(index, masses_[last]);
        add(last, -masses_[last]);
        masses_.pop_back();
    }

    void split(std::size_t index) {
        const Real half = masses_.at(index) / 2;
        replace(index, half);
        append(half);
    }

    void merge(std::size_t first, std::size_t second) {
        require(first < size() && second < size() && first != second, "Invalid pair");
        if (first > second) std::swap(first, second);
        replace(first, masses_[first] + masses_[second]);
        remove(second);  // Keeping the lower index makes swap-removal unambiguous.
    }

    // Return the first index with cumulative mass strictly greater than target.
    std::size_t select(Real target) const {
        require(target >= 0 && target < total(), "Weighted target out of range");
        std::size_t index = 0, bit = 1;
        while (bit < tree_.size()) bit <<= 1;
        for (bit >>= 1; bit > 0; bit >>= 1) {
            const auto next = index + bit;
            if (next < tree_.size() && tree_[next] <= target) {
                index = next;
                target -= tree_[next];
            }
        }
        require(index < size(), "Weighted selection escaped active particles");
        return index;
    }
};

static Real uniform01(std::mt19937_64& rng) {
    return static_cast<Real>(rng() >> 11) * 0x1.0p-53L;
}

static std::size_t uniform_index(std::mt19937_64& rng, std::size_t size) {
    return std::uniform_int_distribution<std::size_t>(0, size - 1)(rng);
}

static void check_tree(const Particles& particles) {
    Real sum = 0;
    for (std::size_t i = 0; i < particles.size(); ++i) {
        const auto mass = particles.masses()[i];
        require(particles.select(sum + mass / 2) == i, "Fenwick interval selection failed");
        sum += mass;
    }
    require(std::abs(sum - particles.total()) < 1e-13L * (1 + sum), "Fenwick mass mismatch");
}

static void self_test() {
    Particles particles(1);
    for (Real mass : {1.L, 2.L, 4.L, 8.L}) particles.append(mass);
    check_tree(particles);  // Includes multiple capacity increases.
    particles.merge(3, 1);
    check_tree(particles);  // Also checks keeping the lower of the selected indices.
    particles.split(0);
    check_tree(particles);
    particles.remove(1);
    check_tree(particles);  // Exercise moving the last particle into an interior slot.
    particles.append(3.L);
    check_tree(particles);

    // Enumerate unordered rates from the two-stage sampler on unequal masses.
    const std::vector<Real> masses = {1.L, 2.L, 4.L, 8.L};
    const Real total = 15, count = masses.size();
    Real pair_rate = 0;
    for (std::size_t i = 0; i < masses.size(); ++i) {
        for (std::size_t j = i + 1; j < masses.size(); ++j) {
            const Real sampler_rate = (count - 1) *
                (masses[i] / total / (count - 1) + masses[j] / total / (count - 1));
            const Real desired_rate = (masses[i] + masses[j]) / total;
            require(std::abs(sampler_rate - desired_rate) < 1e-17L, "Pair rate mismatch");
            pair_rate += desired_rate;
        }
    }
    require(std::abs(pair_rate - (count - 1)) < 1e-17L, "Total coagulation rate mismatch");
    require(count - pair_rate == 1, "Count drift mismatch");
    const Real square_drift = count * (2 * count + 1) + pair_rate * (-2 * count + 1);
    require(std::abs(square_drift - (4 * count - 1)) < 1e-16L, "Count second-moment drift mismatch");

    // Verify that a long sequence of valid events preserves mass and the tree.
    Particles stress(2);
    for (int i = 0; i < 32; ++i) stress.append(1);
    std::mt19937_64 rng(90210);
    for (int k = 0; k < 10000; ++k) {
        if (stress.size() < 2 || (stress.size() < 80 && uniform01(rng) < .5L)) {
            stress.split(uniform_index(rng, stress.size()));
        } else {
            const auto first = stress.select(uniform01(rng) * stress.total());
            auto second = uniform_index(rng, stress.size() - 1);
            if (second >= first) ++second;
            stress.merge(first, second);
        }
        require(std::abs(stress.total() - 32) < 1e-11L, "Event mass conservation failed");
    }
    check_tree(stress);
    std::cout << "self-test passed: weighted intervals, resizing, removals, pair rates, count drift, conservation\n";
}

static void snapshot(const Particles& particles, std::size_t initial_count,
                     std::uint64_t seed, Real time, std::uint64_t births,
                     std::uint64_t deaths) {
    const Real n = initial_count, count = particles.size();
    Real mass = 0, half = 0, log_sum = 0, largest = 0;
    Real smallest = std::numeric_limits<Real>::infinity();
    Real number_small = 0, number_tiny = 0;
    Real mass_one = 0, mass_ten = 0, mass_hundred = 0, mass_thousand = 0;
    Real mass_fraction_01 = 0, mass_fraction_10 = 0;
    for (Real x : particles.masses()) {
        mass += x;
        half += std::sqrt(x);
        log_sum += std::log(x);
        largest = std::max(largest, x);
        smallest = std::min(smallest, x);
        if (x <= .01L) ++number_small;
        if (x <= .0001L) ++number_tiny;
        if (x <= 1) mass_one += x;
        if (x <= 10) mass_ten += x;
        if (x <= 100) mass_hundred += x;
        if (x <= 1000) mass_thousand += x;
        if (x <= .01L * n) mass_fraction_01 += x;
        if (x <= .1L * n) mass_fraction_10 += x;
    }
    const Real log_mean = log_sum / count;
    Real log_variance = 0;
    for (Real x : particles.masses()) {
        const Real difference = std::log(x) - log_mean;
        log_variance += difference * difference;
    }
    log_variance /= count;
    require(particles.size() == initial_count + births - deaths, "Event count identity failed");
    require(std::abs(mass / n - 1) < 1e-10L, "Snapshot mass conservation failed");
    require(std::abs(particles.total() - mass) / n < 1e-10L, "Snapshot tree mass failed");
    require(largest <= n * (1 + 1e-10L), "Physical support bound failed");
    std::cout << initial_count << ',' << seed << ',' << time << ',' << count << ','
        << births << ',' << deaths << ',' << count / n << ',' << mass / n << ','
        << half / n << ',' << log_mean << ',' << log_variance << ',' << largest / n << ','
        << smallest << ',' << number_small / count << ',' << number_tiny / count << ','
        << mass_one / n << ',' << mass_ten / n << ',' << mass_hundred / n << ','
        << mass_thousand / n << ',' << mass_fraction_01 / n << ',' << mass_fraction_10 / n << '\n';
}

int main(int argc, char** argv) {
    try {
        std::cout << std::setprecision(18);
        if (argc == 2 && std::string(argv[1]) == "--self-test") {
            self_test();
            return 0;
        }
        require(argc == 3, "Usage: critical_particles INITIAL_COUNT SEED, or --self-test");
        const auto n = std::stoull(argv[1]);
        const auto seed = std::stoull(argv[2]);
        require(n > 0 && n <= 10000000, "Initial count must lie in [1,10000000]");
        Particles particles(2 * n + 32);
        for (std::size_t i = 0; i < n; ++i) particles.append(1);
        std::mt19937_64 rng(seed);
        const std::vector<Real> times = {0, .5L, 1, 2, 3, 4, 5, 6, 8, 10};
        std::size_t next_snapshot = 0;
        Real time = 0;
        std::uint64_t births = 0, deaths = 0;
        std::cout << "n,seed,time,count,births,deaths,normalized_count,normalized_mass,M_half,"
            "log_mean,log_variance,largest_mass_fraction,min_size,number_CDF_0.01,number_CDF_0.0001,"
            "mass_CDF_1,mass_CDF_10,mass_CDF_100,mass_CDF_1000,mass_CDF_0.01n,mass_CDF_0.1n\n";
        while (next_snapshot < times.size()) {
            const Real count = particles.size();
            const Real rate = 2 * count - 1;
            const Real next_event = time - std::log1p(-uniform01(rng)) / rate;
            // States are constant between events; do not restart an event clock at an output time.
            while (next_snapshot < times.size() && times[next_snapshot] < next_event) {
                snapshot(particles, n, seed, times[next_snapshot], births, deaths);
                ++next_snapshot;
            }
            if (next_snapshot == times.size()) break;
            time = next_event;
            if (uniform01(rng) * rate < count) {
                particles.split(uniform_index(rng, particles.size()));
                ++births;
            } else {
                const auto first = particles.select(uniform01(rng) * particles.total());
                auto second = uniform_index(rng, particles.size() - 1);
                if (second >= first) ++second;
                particles.merge(first, second);
                ++deaths;
            }
        }
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
