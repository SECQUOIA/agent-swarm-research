// Lean compiler output
// Module: Formal.QuadraticAggregation.Hyperplanes
// Imports: public import Init public meta import Init public import Formal.QuadraticAggregation.Recession public import Mathlib.Analysis.LocallyConvex.Separation public import Mathlib.Analysis.Convex.Topology public import Mathlib.LinearAlgebra.Pi public import Mathlib.Algebra.BigOperators.Field
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
lean_object* initialize_formal_Formal_QuadraticAggregation_Recession(uint8_t builtin);
lean_object* initialize_mathlib_Mathlib_Analysis_LocallyConvex_Separation(uint8_t builtin);
lean_object* initialize_mathlib_Mathlib_Analysis_Convex_Topology(uint8_t builtin);
lean_object* initialize_mathlib_Mathlib_LinearAlgebra_Pi(uint8_t builtin);
lean_object* initialize_mathlib_Mathlib_Algebra_BigOperators_Field(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_formal_Formal_QuadraticAggregation_Hyperplanes(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_formal_Formal_QuadraticAggregation_Recession(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_mathlib_Mathlib_Analysis_LocallyConvex_Separation(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_mathlib_Mathlib_Analysis_Convex_Topology(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_mathlib_Mathlib_LinearAlgebra_Pi(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_mathlib_Mathlib_Algebra_BigOperators_Field(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
