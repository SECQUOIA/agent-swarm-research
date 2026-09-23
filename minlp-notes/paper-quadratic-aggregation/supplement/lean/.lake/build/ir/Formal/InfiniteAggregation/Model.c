// Lean compiler output
// Module: Formal.InfiniteAggregation.Model
// Imports: public import Init public meta import Init public import Mathlib
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
lean_object* lp_mathlib_Real_definition___lam__0_00___x40_Mathlib_Data_Real_Basic_4214226450____hygCtx___hyg_8_(lean_object*, lean_object*, lean_object*);
lean_object* l_List_finRange(lean_object*);
lean_object* lp_mathlib_Finset_sum___at___00BoundingSieve_multSum_spec__0___redArg(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_dotProduct___at___00InfiniteAggregation_dot_spec__0___lam__0(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_dotProduct___at___00InfiniteAggregation_dot_spec__0(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_dot(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_qnorm(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_dotProduct___at___00InfiniteAggregation_dot_spec__0___lam__0(lean_object* v_v_1_, lean_object* v_w_2_, lean_object* v_i_3_){
_start:
{
lean_object* v___x_4_; lean_object* v___x_5_; lean_object* v___f_6_; 
lean_inc(v_i_3_);
v___x_4_ = lean_apply_1(v_v_1_, v_i_3_);
v___x_5_ = lean_apply_1(v_w_2_, v_i_3_);
v___f_6_ = lean_alloc_closure((void*)(lp_mathlib_Real_definition___lam__0_00___x40_Mathlib_Data_Real_Basic_4214226450____hygCtx___hyg_8_), 3, 2);
lean_closure_set(v___f_6_, 0, v___x_4_);
lean_closure_set(v___f_6_, 1, v___x_5_);
return v___f_6_;
}
}
LEAN_EXPORT lean_object* lp_formal_dotProduct___at___00InfiniteAggregation_dot_spec__0(lean_object* v_r_7_, lean_object* v_v_8_, lean_object* v_w_9_){
_start:
{
lean_object* v___f_10_; lean_object* v___x_11_; lean_object* v___x_12_; 
v___f_10_ = lean_alloc_closure((void*)(lp_formal_dotProduct___at___00InfiniteAggregation_dot_spec__0___lam__0), 3, 2);
lean_closure_set(v___f_10_, 0, v_v_8_);
lean_closure_set(v___f_10_, 1, v_w_9_);
v___x_11_ = l_List_finRange(v_r_7_);
v___x_12_ = lp_mathlib_Finset_sum___at___00BoundingSieve_multSum_spec__0___redArg(v___x_11_, v___f_10_);
return v___x_12_;
}
}
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_dot(lean_object* v_r_13_, lean_object* v_u_14_, lean_object* v_v_15_){
_start:
{
lean_object* v___x_16_; 
v___x_16_ = lp_formal_dotProduct___at___00InfiniteAggregation_dot_spec__0(v_r_13_, v_u_14_, v_v_15_);
return v___x_16_;
}
}
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_qnorm(lean_object* v_r_17_, lean_object* v_u_18_){
_start:
{
lean_object* v___x_19_; 
lean_inc(v_u_18_);
v___x_19_ = lp_formal_dotProduct___at___00InfiniteAggregation_dot_spec__0(v_r_17_, v_u_18_, v_u_18_);
return v___x_19_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_mathlib_Mathlib(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_formal_Formal_InfiniteAggregation_Model(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_mathlib_Mathlib(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
