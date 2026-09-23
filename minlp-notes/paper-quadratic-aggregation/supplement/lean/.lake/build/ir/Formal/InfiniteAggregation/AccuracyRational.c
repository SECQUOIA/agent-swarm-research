// Lean compiler output
// Module: Formal.InfiniteAggregation.AccuracyRational
// Imports: public import Init public meta import Init public import Formal.InfiniteAggregation.Good
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
lean_object* lean_nat_pow(lean_object*, lean_object*);
lean_object* lean_nat_mul(lean_object*, lean_object*);
lean_object* l_Fin_cases___redArg(lean_object*, lean_object*, lean_object*);
lean_object* lp_mathlib_Nat_cast___at___00Nat_cast___at___00Nat_cast___at___00Nat_cast___at___00__private_Mathlib_NumberTheory_ModularForms_EisensteinSeries_E2_Transform_0__EisensteinSeries_00_u03b4_spec__0_spec__0_spec__2_spec__3(lean_object*);
lean_object* lean_nat_sub(lean_object*, lean_object*);
lean_object* lean_nat_shiftr(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_rationalLeftCoeff___lam__0(lean_object*);
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_rationalLeftCoeff___lam__0___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_rationalLeftCoeff___lam__1(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_rationalLeftCoeff___lam__1___boxed(lean_object*, lean_object*, lean_object*);
static const lean_closure_object lp_formal_InfiniteAggregation_rationalLeftCoeff___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_formal_InfiniteAggregation_rationalLeftCoeff___lam__0___boxed, .m_arity = 1, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_formal_InfiniteAggregation_rationalLeftCoeff___closed__0 = (const lean_object*)&lp_formal_InfiniteAggregation_rationalLeftCoeff___closed__0_value;
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_rationalLeftCoeff(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_rationalLeftCoeff___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_rationalRightCoeff(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_rationalRightCoeff___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_rationalLeft(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_rationalLeft___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_rationalRight(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_rationalRight___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_rationalMeshSize(lean_object*);
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_rationalMeshSize___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_rationalLeftCoeff___lam__0(lean_object* v___y_1_){
_start:
{
lean_internal_panic_unreachable();
}
}
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_rationalLeftCoeff___lam__0___boxed(lean_object* v___y_2_){
_start:
{
lean_object* v_res_3_; 
v_res_3_ = lp_formal_InfiniteAggregation_rationalLeftCoeff___lam__0(v___y_2_);
lean_dec(v___y_2_);
return v_res_3_;
}
}
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_rationalLeftCoeff___lam__1(lean_object* v___x_4_, lean_object* v___f_5_, lean_object* v___y_6_){
_start:
{
lean_object* v___x_7_; 
v___x_7_ = l_Fin_cases___redArg(v___x_4_, v___f_5_, v___y_6_);
return v___x_7_;
}
}
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_rationalLeftCoeff___lam__1___boxed(lean_object* v___x_8_, lean_object* v___f_9_, lean_object* v___y_10_){
_start:
{
lean_object* v_res_11_; 
v_res_11_ = lp_formal_InfiniteAggregation_rationalLeftCoeff___lam__1(v___x_8_, v___f_9_, v___y_10_);
lean_dec(v___y_10_);
lean_dec(v___x_8_);
return v_res_11_;
}
}
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_rationalLeftCoeff(lean_object* v_m_13_, lean_object* v_j_14_, lean_object* v_a_15_){
_start:
{
lean_object* v___f_16_; lean_object* v___x_17_; lean_object* v___x_18_; lean_object* v___x_19_; lean_object* v___x_20_; lean_object* v___x_21_; lean_object* v___f_22_; lean_object* v___f_23_; lean_object* v___x_24_; 
v___f_16_ = ((lean_object*)(lp_formal_InfiniteAggregation_rationalLeftCoeff___closed__0));
v___x_17_ = lean_unsigned_to_nat(2u);
v___x_18_ = lean_nat_pow(v_m_13_, v___x_17_);
v___x_19_ = lean_nat_pow(v_j_14_, v___x_17_);
v___x_20_ = lean_nat_mul(v___x_17_, v_m_13_);
v___x_21_ = lean_nat_mul(v___x_20_, v_j_14_);
lean_dec(v___x_20_);
v___f_22_ = lean_alloc_closure((void*)(lp_formal_InfiniteAggregation_rationalLeftCoeff___lam__1___boxed), 3, 2);
lean_closure_set(v___f_22_, 0, v___x_21_);
lean_closure_set(v___f_22_, 1, v___f_16_);
v___f_23_ = lean_alloc_closure((void*)(lp_formal_InfiniteAggregation_rationalLeftCoeff___lam__1___boxed), 3, 2);
lean_closure_set(v___f_23_, 0, v___x_19_);
lean_closure_set(v___f_23_, 1, v___f_22_);
v___x_24_ = l_Fin_cases___redArg(v___x_18_, v___f_23_, v_a_15_);
lean_dec(v___x_18_);
return v___x_24_;
}
}
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_rationalLeftCoeff___boxed(lean_object* v_m_25_, lean_object* v_j_26_, lean_object* v_a_27_){
_start:
{
lean_object* v_res_28_; 
v_res_28_ = lp_formal_InfiniteAggregation_rationalLeftCoeff(v_m_25_, v_j_26_, v_a_27_);
lean_dec(v_a_27_);
lean_dec(v_j_26_);
lean_dec(v_m_25_);
return v_res_28_;
}
}
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_rationalRightCoeff(lean_object* v_m_29_, lean_object* v_j_30_, lean_object* v_a_31_){
_start:
{
lean_object* v___f_32_; lean_object* v___x_33_; lean_object* v___x_34_; lean_object* v___x_35_; lean_object* v___x_36_; lean_object* v___x_37_; lean_object* v___f_38_; lean_object* v___f_39_; lean_object* v___x_40_; 
v___f_32_ = ((lean_object*)(lp_formal_InfiniteAggregation_rationalLeftCoeff___closed__0));
v___x_33_ = lean_unsigned_to_nat(2u);
v___x_34_ = lean_nat_pow(v_j_30_, v___x_33_);
v___x_35_ = lean_nat_pow(v_m_29_, v___x_33_);
v___x_36_ = lean_nat_mul(v___x_33_, v_m_29_);
v___x_37_ = lean_nat_mul(v___x_36_, v_j_30_);
lean_dec(v___x_36_);
v___f_38_ = lean_alloc_closure((void*)(lp_formal_InfiniteAggregation_rationalLeftCoeff___lam__1___boxed), 3, 2);
lean_closure_set(v___f_38_, 0, v___x_37_);
lean_closure_set(v___f_38_, 1, v___f_32_);
v___f_39_ = lean_alloc_closure((void*)(lp_formal_InfiniteAggregation_rationalLeftCoeff___lam__1___boxed), 3, 2);
lean_closure_set(v___f_39_, 0, v___x_35_);
lean_closure_set(v___f_39_, 1, v___f_38_);
v___x_40_ = l_Fin_cases___redArg(v___x_34_, v___f_39_, v_a_31_);
lean_dec(v___x_34_);
return v___x_40_;
}
}
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_rationalRightCoeff___boxed(lean_object* v_m_41_, lean_object* v_j_42_, lean_object* v_a_43_){
_start:
{
lean_object* v_res_44_; 
v_res_44_ = lp_formal_InfiniteAggregation_rationalRightCoeff(v_m_41_, v_j_42_, v_a_43_);
lean_dec(v_a_43_);
lean_dec(v_j_42_);
lean_dec(v_m_41_);
return v_res_44_;
}
}
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_rationalLeft(lean_object* v_m_45_, lean_object* v_j_46_, lean_object* v_i_47_){
_start:
{
lean_object* v___x_48_; lean_object* v___x_49_; 
v___x_48_ = lp_formal_InfiniteAggregation_rationalLeftCoeff(v_m_45_, v_j_46_, v_i_47_);
v___x_49_ = lp_mathlib_Nat_cast___at___00Nat_cast___at___00Nat_cast___at___00Nat_cast___at___00__private_Mathlib_NumberTheory_ModularForms_EisensteinSeries_E2_Transform_0__EisensteinSeries_00_u03b4_spec__0_spec__0_spec__2_spec__3(v___x_48_);
return v___x_49_;
}
}
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_rationalLeft___boxed(lean_object* v_m_50_, lean_object* v_j_51_, lean_object* v_i_52_){
_start:
{
lean_object* v_res_53_; 
v_res_53_ = lp_formal_InfiniteAggregation_rationalLeft(v_m_50_, v_j_51_, v_i_52_);
lean_dec(v_i_52_);
lean_dec(v_j_51_);
lean_dec(v_m_50_);
return v_res_53_;
}
}
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_rationalRight(lean_object* v_m_54_, lean_object* v_j_55_, lean_object* v_i_56_){
_start:
{
lean_object* v___x_57_; lean_object* v___x_58_; 
v___x_57_ = lp_formal_InfiniteAggregation_rationalRightCoeff(v_m_54_, v_j_55_, v_i_56_);
v___x_58_ = lp_mathlib_Nat_cast___at___00Nat_cast___at___00Nat_cast___at___00Nat_cast___at___00__private_Mathlib_NumberTheory_ModularForms_EisensteinSeries_E2_Transform_0__EisensteinSeries_00_u03b4_spec__0_spec__0_spec__2_spec__3(v___x_57_);
return v___x_58_;
}
}
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_rationalRight___boxed(lean_object* v_m_59_, lean_object* v_j_60_, lean_object* v_i_61_){
_start:
{
lean_object* v_res_62_; 
v_res_62_ = lp_formal_InfiniteAggregation_rationalRight(v_m_59_, v_j_60_, v_i_61_);
lean_dec(v_i_61_);
lean_dec(v_j_60_);
lean_dec(v_m_59_);
return v_res_62_;
}
}
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_rationalMeshSize(lean_object* v_N_63_){
_start:
{
lean_object* v___x_64_; lean_object* v___x_65_; lean_object* v___x_66_; 
v___x_64_ = lean_unsigned_to_nat(1u);
v___x_65_ = lean_nat_sub(v_N_63_, v___x_64_);
v___x_66_ = lean_nat_shiftr(v___x_65_, v___x_64_);
lean_dec(v___x_65_);
return v___x_66_;
}
}
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_rationalMeshSize___boxed(lean_object* v_N_67_){
_start:
{
lean_object* v_res_68_; 
v_res_68_ = lp_formal_InfiniteAggregation_rationalMeshSize(v_N_67_);
lean_dec(v_N_67_);
return v_res_68_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_formal_Formal_InfiniteAggregation_Good(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_formal_Formal_InfiniteAggregation_AccuracyRational(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_formal_Formal_InfiniteAggregation_Good(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
