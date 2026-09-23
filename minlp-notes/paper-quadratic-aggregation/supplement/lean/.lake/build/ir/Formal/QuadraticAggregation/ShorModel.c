// Lean compiler output
// Module: Formal.QuadraticAggregation.ShorModel
// Imports: public import Init public meta import Init public import Formal.QuadraticAggregation.ShorBlock
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
lean_object* l_List_finRange(lean_object*);
lean_object* lp_mathlib_Finset_sum___at___00BoundingSieve_multSum_spec__0___redArg(lean_object*, lean_object*);
lean_object* lp_mathlib_Real_definition___lam__0_00___x40_Mathlib_Data_Real_Basic_4214226450____hygCtx___hyg_8_(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_Matrix_trace___at___00QuadraticAggregation_tracePair_spec__0___lam__0(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_Matrix_trace___at___00QuadraticAggregation_tracePair_spec__0(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_dotProduct___at___00QuadraticAggregation_q_spec__1___at___00QuadraticAggregation_tracePair_spec__1___lam__0(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_dotProduct___at___00QuadraticAggregation_q_spec__1___at___00QuadraticAggregation_tracePair_spec__1(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_QuadraticAggregation_tracePair___lam__0(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_QuadraticAggregation_tracePair___lam__1(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_QuadraticAggregation_tracePair(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_Matrix_trace___at___00QuadraticAggregation_tracePair_spec__0___lam__0(lean_object* v_A_1_, lean_object* v_i_2_){
_start:
{
lean_object* v___x_3_; 
lean_inc(v_i_2_);
v___x_3_ = lean_apply_2(v_A_1_, v_i_2_, v_i_2_);
return v___x_3_;
}
}
LEAN_EXPORT lean_object* lp_formal_Matrix_trace___at___00QuadraticAggregation_tracePair_spec__0(lean_object* v_n_4_, lean_object* v_A_5_){
_start:
{
lean_object* v___f_6_; lean_object* v___x_7_; lean_object* v___x_8_; 
v___f_6_ = lean_alloc_closure((void*)(lp_formal_Matrix_trace___at___00QuadraticAggregation_tracePair_spec__0___lam__0), 2, 1);
lean_closure_set(v___f_6_, 0, v_A_5_);
v___x_7_ = l_List_finRange(v_n_4_);
v___x_8_ = lp_mathlib_Finset_sum___at___00BoundingSieve_multSum_spec__0___redArg(v___x_7_, v___f_6_);
return v___x_8_;
}
}
LEAN_EXPORT lean_object* lp_formal_dotProduct___at___00QuadraticAggregation_q_spec__1___at___00QuadraticAggregation_tracePair_spec__1___lam__0(lean_object* v_A_9_, lean_object* v___y_10_, lean_object* v_w_11_, lean_object* v_i_12_){
_start:
{
lean_object* v___x_13_; lean_object* v___x_14_; lean_object* v___f_15_; 
lean_inc(v_i_12_);
v___x_13_ = lean_apply_2(v_A_9_, v___y_10_, v_i_12_);
v___x_14_ = lean_apply_1(v_w_11_, v_i_12_);
v___f_15_ = lean_alloc_closure((void*)(lp_mathlib_Real_definition___lam__0_00___x40_Mathlib_Data_Real_Basic_4214226450____hygCtx___hyg_8_), 3, 2);
lean_closure_set(v___f_15_, 0, v___x_13_);
lean_closure_set(v___f_15_, 1, v___x_14_);
return v___f_15_;
}
}
LEAN_EXPORT lean_object* lp_formal_dotProduct___at___00QuadraticAggregation_q_spec__1___at___00QuadraticAggregation_tracePair_spec__1(lean_object* v_A_16_, lean_object* v___y_17_, lean_object* v_n_18_, lean_object* v_w_19_){
_start:
{
lean_object* v___f_20_; lean_object* v___x_21_; lean_object* v___x_22_; 
v___f_20_ = lean_alloc_closure((void*)(lp_formal_dotProduct___at___00QuadraticAggregation_q_spec__1___at___00QuadraticAggregation_tracePair_spec__1___lam__0), 4, 3);
lean_closure_set(v___f_20_, 0, v_A_16_);
lean_closure_set(v___f_20_, 1, v___y_17_);
lean_closure_set(v___f_20_, 2, v_w_19_);
v___x_21_ = l_List_finRange(v_n_18_);
v___x_22_ = lp_mathlib_Finset_sum___at___00BoundingSieve_multSum_spec__0___redArg(v___x_21_, v___f_20_);
return v___x_22_;
}
}
LEAN_EXPORT lean_object* lp_formal_QuadraticAggregation_tracePair___lam__0(lean_object* v_Y_23_, lean_object* v___y_24_, lean_object* v_j_25_){
_start:
{
lean_object* v___x_26_; 
v___x_26_ = lean_apply_2(v_Y_23_, v_j_25_, v___y_24_);
return v___x_26_;
}
}
LEAN_EXPORT lean_object* lp_formal_QuadraticAggregation_tracePair___lam__1(lean_object* v_Y_27_, lean_object* v_A_28_, lean_object* v_n_29_, lean_object* v___y_30_, lean_object* v___y_31_){
_start:
{
lean_object* v___f_32_; lean_object* v___x_33_; 
v___f_32_ = lean_alloc_closure((void*)(lp_formal_QuadraticAggregation_tracePair___lam__0), 3, 2);
lean_closure_set(v___f_32_, 0, v_Y_27_);
lean_closure_set(v___f_32_, 1, v___y_31_);
v___x_33_ = lp_formal_dotProduct___at___00QuadraticAggregation_q_spec__1___at___00QuadraticAggregation_tracePair_spec__1(v_A_28_, v___y_30_, v_n_29_, v___f_32_);
return v___x_33_;
}
}
LEAN_EXPORT lean_object* lp_formal_QuadraticAggregation_tracePair(lean_object* v_n_34_, lean_object* v_A_35_, lean_object* v_Y_36_){
_start:
{
lean_object* v___f_37_; lean_object* v___x_38_; 
lean_inc(v_n_34_);
v___f_37_ = lean_alloc_closure((void*)(lp_formal_QuadraticAggregation_tracePair___lam__1), 5, 3);
lean_closure_set(v___f_37_, 0, v_Y_36_);
lean_closure_set(v___f_37_, 1, v_A_35_);
lean_closure_set(v___f_37_, 2, v_n_34_);
v___x_38_ = lp_formal_Matrix_trace___at___00QuadraticAggregation_tracePair_spec__0(v_n_34_, v___f_37_);
return v___x_38_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_formal_Formal_QuadraticAggregation_ShorBlock(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_formal_Formal_QuadraticAggregation_ShorModel(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_formal_Formal_QuadraticAggregation_ShorBlock(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
