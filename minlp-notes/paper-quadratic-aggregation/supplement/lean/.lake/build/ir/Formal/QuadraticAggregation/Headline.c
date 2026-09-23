// Lean compiler output
// Module: Formal.QuadraticAggregation.Headline
// Imports: public import Init public meta import Init public import Formal.QuadraticAggregation.Coefficients public import Formal.QuadraticAggregation.LimitCompactness public import Formal.QuadraticAggregation.SweepBounds public import Formal.QuadraticAggregation.Hyperplanes public import Formal.QuadraticAggregation.EasyDirection public import Formal.QuadraticAggregation.DefinitionsSequence
#include <lean/lean.h>
#if defined(__clang__)
#pragma clang diagnostic ignored "-Wunused-parameter"
#pragma clang diagnostic ignored "-Wunused-label"
#elif defined(__GNUC__) && !defined(__CLANG__)
#pragma GCC diagnostic ignored "-Wunused-parameter"
#pragma GCC diagnostic ignored "-Wunused-label"
#pragma GCC diagnostic ignored "-Wunused-but-set-variable"
#endif
#ifdef __cplusplus
extern "C" {
#endif
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_formal_Formal_QuadraticAggregation_Coefficients(uint8_t builtin);
lean_object* initialize_formal_Formal_QuadraticAggregation_LimitCompactness(uint8_t builtin);
lean_object* initialize_formal_Formal_QuadraticAggregation_SweepBounds(uint8_t builtin);
lean_object* initialize_formal_Formal_QuadraticAggregation_Hyperplanes(uint8_t builtin);
lean_object* initialize_formal_Formal_QuadraticAggregation_EasyDirection(uint8_t builtin);
lean_object* initialize_formal_Formal_QuadraticAggregation_DefinitionsSequence(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_formal_Formal_QuadraticAggregation_Headline(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_formal_Formal_QuadraticAggregation_Coefficients(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_formal_Formal_QuadraticAggregation_LimitCompactness(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_formal_Formal_QuadraticAggregation_SweepBounds(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_formal_Formal_QuadraticAggregation_Hyperplanes(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_formal_Formal_QuadraticAggregation_EasyDirection(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_formal_Formal_QuadraticAggregation_DefinitionsSequence(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
