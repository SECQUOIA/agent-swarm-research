// Lean compiler output
// Module: Formal.InfiniteAggregation.AccuracyModel
// Imports: public import Init public meta import Init public import Formal.InfiniteAggregation.HullRepresentations
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
lean_object* l_Sum_elim(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_euclidean___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_euclidean(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_euclidean___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_euclidean___redArg(lean_object* v_x_1_){
_start:
{
lean_object* v_fst_2_; lean_object* v_snd_3_; lean_object* v___x_4_; 
v_fst_2_ = lean_ctor_get(v_x_1_, 0);
lean_inc(v_fst_2_);
v_snd_3_ = lean_ctor_get(v_x_1_, 1);
lean_inc(v_snd_3_);
lean_dec_ref(v_x_1_);
v___x_4_ = lean_alloc_closure((void*)(l_Sum_elim), 6, 5);
lean_closure_set(v___x_4_, 0, lean_box(0));
lean_closure_set(v___x_4_, 1, lean_box(0));
lean_closure_set(v___x_4_, 2, lean_box(0));
lean_closure_set(v___x_4_, 3, v_fst_2_);
lean_closure_set(v___x_4_, 4, v_snd_3_);
return v___x_4_;
}
}
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_euclidean(lean_object* v_r_5_, lean_object* v_x_6_){
_start:
{
lean_object* v___x_7_; 
v___x_7_ = lp_formal_InfiniteAggregation_euclidean___redArg(v_x_6_);
return v___x_7_;
}
}
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_euclidean___boxed(lean_object* v_r_8_, lean_object* v_x_9_){
_start:
{
lean_object* v_res_10_; 
v_res_10_ = lp_formal_InfiniteAggregation_euclidean(v_r_8_, v_x_9_);
lean_dec(v_r_8_);
return v_res_10_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_formal_Formal_InfiniteAggregation_HullRepresentations(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_formal_Formal_InfiniteAggregation_AccuracyModel(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_formal_Formal_InfiniteAggregation_HullRepresentations(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
