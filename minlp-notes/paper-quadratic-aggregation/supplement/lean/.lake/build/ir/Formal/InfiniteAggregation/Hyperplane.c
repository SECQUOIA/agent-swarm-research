// Lean compiler output
// Module: Formal.InfiniteAggregation.Hyperplane
// Imports: public import Init public meta import Init public import Formal.InfiniteAggregation.Model public import Formal.InfiniteAggregation.GramConcavity
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
lean_object* lp_mathlib_npowRec___at___00Cardinal_cantorFunctionAux_spec__0(lean_object*, lean_object*);
lean_object* l_Fin_cases___redArg(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_dotProduct___at___00InfiniteAggregation_dot_spec__0___at___00InfiniteAggregation_homGram_spec__0___lam__0(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_dotProduct___at___00InfiniteAggregation_dot_spec__0___at___00InfiniteAggregation_homGram_spec__0(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_dotProduct___at___00InfiniteAggregation_dot_spec__0___at___00InfiniteAggregation_homGram_spec__1___lam__0(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_dotProduct___at___00InfiniteAggregation_dot_spec__0___at___00InfiniteAggregation_homGram_spec__1(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_homGram___lam__0(lean_object*);
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_homGram___lam__0___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_homGram___lam__1(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_homGram___lam__1___boxed(lean_object*, lean_object*, lean_object*);
static const lean_closure_object lp_formal_InfiniteAggregation_homGram___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_formal_InfiniteAggregation_homGram___lam__0___boxed, .m_arity = 1, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_formal_InfiniteAggregation_homGram___closed__0 = (const lean_object*)&lp_formal_InfiniteAggregation_homGram___closed__0_value;
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_homGram(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_homGram___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_dotProduct___at___00InfiniteAggregation_dot_spec__0___at___00InfiniteAggregation_homGram_spec__0___lam__0(lean_object* v___x_1_, lean_object* v_i_2_){
_start:
{
lean_object* v___x_3_; lean_object* v___f_4_; 
v___x_3_ = lean_apply_1(v___x_1_, v_i_2_);
lean_inc(v___x_3_);
v___f_4_ = lean_alloc_closure((void*)(lp_mathlib_Real_definition___lam__0_00___x40_Mathlib_Data_Real_Basic_4214226450____hygCtx___hyg_8_), 3, 2);
lean_closure_set(v___f_4_, 0, v___x_3_);
lean_closure_set(v___f_4_, 1, v___x_3_);
return v___f_4_;
}
}
LEAN_EXPORT lean_object* lp_formal_dotProduct___at___00InfiniteAggregation_dot_spec__0___at___00InfiniteAggregation_homGram_spec__0(lean_object* v___x_5_, lean_object* v_r_6_){
_start:
{
lean_object* v___f_7_; lean_object* v___x_8_; lean_object* v___x_9_; 
v___f_7_ = lean_alloc_closure((void*)(lp_formal_dotProduct___at___00InfiniteAggregation_dot_spec__0___at___00InfiniteAggregation_homGram_spec__0___lam__0), 2, 1);
lean_closure_set(v___f_7_, 0, v___x_5_);
v___x_8_ = l_List_finRange(v_r_6_);
v___x_9_ = lp_mathlib_Finset_sum___at___00BoundingSieve_multSum_spec__0___redArg(v___x_8_, v___f_7_);
return v___x_9_;
}
}
LEAN_EXPORT lean_object* lp_formal_dotProduct___at___00InfiniteAggregation_dot_spec__0___at___00InfiniteAggregation_homGram_spec__1___lam__0(lean_object* v___x_10_, lean_object* v___x_11_, lean_object* v_i_12_){
_start:
{
lean_object* v___x_13_; lean_object* v___x_14_; lean_object* v___f_15_; 
lean_inc(v_i_12_);
v___x_13_ = lean_apply_1(v___x_10_, v_i_12_);
v___x_14_ = lean_apply_1(v___x_11_, v_i_12_);
v___f_15_ = lean_alloc_closure((void*)(lp_mathlib_Real_definition___lam__0_00___x40_Mathlib_Data_Real_Basic_4214226450____hygCtx___hyg_8_), 3, 2);
lean_closure_set(v___f_15_, 0, v___x_13_);
lean_closure_set(v___f_15_, 1, v___x_14_);
return v___f_15_;
}
}
LEAN_EXPORT lean_object* lp_formal_dotProduct___at___00InfiniteAggregation_dot_spec__0___at___00InfiniteAggregation_homGram_spec__1(lean_object* v___x_16_, lean_object* v___x_17_, lean_object* v_r_18_){
_start:
{
lean_object* v___f_19_; lean_object* v___x_20_; lean_object* v___x_21_; 
v___f_19_ = lean_alloc_closure((void*)(lp_formal_dotProduct___at___00InfiniteAggregation_dot_spec__0___at___00InfiniteAggregation_homGram_spec__1___lam__0), 3, 2);
lean_closure_set(v___f_19_, 0, v___x_16_);
lean_closure_set(v___f_19_, 1, v___x_17_);
v___x_20_ = l_List_finRange(v_r_18_);
v___x_21_ = lp_mathlib_Finset_sum___at___00BoundingSieve_multSum_spec__0___redArg(v___x_20_, v___f_19_);
return v___x_21_;
}
}
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_homGram___lam__0(lean_object* v___y_22_){
_start:
{
lean_internal_panic_unreachable();
}
}
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_homGram___lam__0___boxed(lean_object* v___y_23_){
_start:
{
lean_object* v_res_24_; 
v_res_24_ = lp_formal_InfiniteAggregation_homGram___lam__0(v___y_23_);
lean_dec(v___y_23_);
return v_res_24_;
}
}
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_homGram___lam__1(lean_object* v___x_25_, lean_object* v___f_26_, lean_object* v___y_27_){
_start:
{
lean_object* v___x_28_; 
v___x_28_ = l_Fin_cases___redArg(v___x_25_, v___f_26_, v___y_27_);
return v___x_28_;
}
}
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_homGram___lam__1___boxed(lean_object* v___x_29_, lean_object* v___f_30_, lean_object* v___y_31_){
_start:
{
lean_object* v_res_32_; 
v_res_32_ = lp_formal_InfiniteAggregation_homGram___lam__1(v___x_29_, v___f_30_, v___y_31_);
lean_dec(v___y_31_);
lean_dec(v___x_29_);
return v_res_32_;
}
}
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_homGram(lean_object* v_r_34_, lean_object* v_z_35_, lean_object* v_a_36_){
_start:
{
lean_object* v_fst_37_; lean_object* v_snd_38_; lean_object* v_fst_39_; lean_object* v_snd_40_; lean_object* v___f_41_; lean_object* v___x_42_; lean_object* v___x_43_; lean_object* v___x_44_; lean_object* v___x_45_; lean_object* v___x_46_; lean_object* v___f_47_; lean_object* v___f_48_; lean_object* v___f_49_; lean_object* v___x_50_; 
v_fst_37_ = lean_ctor_get(v_z_35_, 0);
lean_inc(v_fst_37_);
v_snd_38_ = lean_ctor_get(v_z_35_, 1);
lean_inc(v_snd_38_);
lean_dec_ref(v_z_35_);
v_fst_39_ = lean_ctor_get(v_fst_37_, 0);
lean_inc_n(v_fst_39_, 2);
v_snd_40_ = lean_ctor_get(v_fst_37_, 1);
lean_inc_n(v_snd_40_, 2);
lean_dec(v_fst_37_);
v___f_41_ = ((lean_object*)(lp_formal_InfiniteAggregation_homGram___closed__0));
lean_inc_n(v_r_34_, 2);
v___x_42_ = lp_formal_dotProduct___at___00InfiniteAggregation_dot_spec__0___at___00InfiniteAggregation_homGram_spec__0(v_fst_39_, v_r_34_);
v___x_43_ = lean_unsigned_to_nat(2u);
v___x_44_ = lp_formal_dotProduct___at___00InfiniteAggregation_dot_spec__0___at___00InfiniteAggregation_homGram_spec__0(v_snd_40_, v_r_34_);
v___x_45_ = lp_formal_dotProduct___at___00InfiniteAggregation_dot_spec__0___at___00InfiniteAggregation_homGram_spec__1(v_fst_39_, v_snd_40_, v_r_34_);
v___x_46_ = lp_mathlib_npowRec___at___00Cardinal_cantorFunctionAux_spec__0(v___x_43_, v_snd_38_);
v___f_47_ = lean_alloc_closure((void*)(lp_formal_InfiniteAggregation_homGram___lam__1___boxed), 3, 2);
lean_closure_set(v___f_47_, 0, v___x_46_);
lean_closure_set(v___f_47_, 1, v___f_41_);
v___f_48_ = lean_alloc_closure((void*)(lp_formal_InfiniteAggregation_homGram___lam__1___boxed), 3, 2);
lean_closure_set(v___f_48_, 0, v___x_45_);
lean_closure_set(v___f_48_, 1, v___f_47_);
v___f_49_ = lean_alloc_closure((void*)(lp_formal_InfiniteAggregation_homGram___lam__1___boxed), 3, 2);
lean_closure_set(v___f_49_, 0, v___x_44_);
lean_closure_set(v___f_49_, 1, v___f_48_);
v___x_50_ = l_Fin_cases___redArg(v___x_42_, v___f_49_, v_a_36_);
lean_dec(v___x_42_);
return v___x_50_;
}
}
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_homGram___boxed(lean_object* v_r_51_, lean_object* v_z_52_, lean_object* v_a_53_){
_start:
{
lean_object* v_res_54_; 
v_res_54_ = lp_formal_InfiniteAggregation_homGram(v_r_51_, v_z_52_, v_a_53_);
lean_dec(v_a_53_);
return v_res_54_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_formal_Formal_InfiniteAggregation_Model(uint8_t builtin);
lean_object* initialize_formal_Formal_InfiniteAggregation_GramConcavity(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_formal_Formal_InfiniteAggregation_Hyperplane(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_formal_Formal_InfiniteAggregation_Model(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_formal_Formal_InfiniteAggregation_GramConcavity(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
