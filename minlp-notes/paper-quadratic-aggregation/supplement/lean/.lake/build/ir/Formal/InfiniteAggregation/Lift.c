// Lean compiler output
// Module: Formal.InfiniteAggregation.Lift
// Imports: public import Init public meta import Init public import Formal.InfiniteAggregation.Model public import Formal.InfiniteAggregation.LiftSmall public import Formal.InfiniteAggregation.HullModel
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
uint8_t lean_nat_dec_eq(lean_object*, lean_object*);
extern lean_object* lp_mathlib_Real_definition_00___x40_Mathlib_Data_Real_Basic_1850581184____hygCtx___hyg_8_;
lean_object* l_Fin_cases___redArg(lean_object*, lean_object*, lean_object*);
lean_object* lp_mathlib_Matrix_transpose(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* lp_mathlib_Matrix_map___redArg(lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* lp_mathlib_Equiv_refl(lean_object*);
extern lean_object* lp_mathlib_Real_definition_00___x40_Mathlib_Data_Real_Basic_1279875089____hygCtx___hyg_8_;
lean_object* lp_mathlib_Real_definition___lam__0_00___x40_Mathlib_Data_Real_Basic_4214226450____hygCtx___hyg_8_(lean_object*, lean_object*, lean_object*);
lean_object* l_List_finRange(lean_object*);
lean_object* lp_mathlib_Finset_sum___at___00BoundingSieve_multSum_spec__0___redArg(lean_object*, lean_object*);
lean_object* lean_nat_mod(lean_object*, lean_object*);
lean_object* lp_mathlib_Matrix_fromBlocks___redArg(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* lp_mathlib_Real_definition___lam__0_00___x40_Mathlib_Data_Real_Basic_2451848184____hygCtx___hyg_8_(lean_object*, lean_object*);
lean_object* lp_mathlib_Real_definition___lam__0_00___x40_Mathlib_Data_Real_Basic_1138242547____hygCtx___hyg_8_(lean_object*, lean_object*, lean_object*);
static lean_once_cell_t lp_formal_InfiniteAggregation_liftRows___redArg___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_formal_InfiniteAggregation_liftRows___redArg___closed__0;
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_liftRows___redArg(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_liftRows___redArg___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_liftRows(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_liftRows___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_Matrix_conjTranspose___at___00InfiniteAggregation_hullLift_spec__0___redArg___lam__0(lean_object*);
LEAN_EXPORT lean_object* lp_formal_Matrix_conjTranspose___at___00InfiniteAggregation_hullLift_spec__0___redArg___lam__0___boxed(lean_object*);
static const lean_closure_object lp_formal_Matrix_conjTranspose___at___00InfiniteAggregation_hullLift_spec__0___redArg___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_formal_Matrix_conjTranspose___at___00InfiniteAggregation_hullLift_spec__0___redArg___lam__0___boxed, .m_arity = 1, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_formal_Matrix_conjTranspose___at___00InfiniteAggregation_hullLift_spec__0___redArg___closed__0 = (const lean_object*)&lp_formal_Matrix_conjTranspose___at___00InfiniteAggregation_hullLift_spec__0___redArg___closed__0_value;
LEAN_EXPORT lean_object* lp_formal_Matrix_conjTranspose___at___00InfiniteAggregation_hullLift_spec__0___redArg(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_Matrix_conjTranspose___at___00InfiniteAggregation_hullLift_spec__0(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_Matrix_diagonal___at___00InfiniteAggregation_hullLift_spec__1___redArg___lam__0(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_Matrix_diagonal___at___00InfiniteAggregation_hullLift_spec__1___redArg___lam__0___boxed(lean_object*, lean_object*, lean_object*);
static lean_once_cell_t lp_formal_Matrix_diagonal___at___00InfiniteAggregation_hullLift_spec__1___redArg___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_formal_Matrix_diagonal___at___00InfiniteAggregation_hullLift_spec__1___redArg___closed__0;
LEAN_EXPORT lean_object* lp_formal_Matrix_diagonal___at___00InfiniteAggregation_hullLift_spec__1___redArg(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_Matrix_diagonal___at___00InfiniteAggregation_hullLift_spec__1(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_Matrix_diagonal___at___00InfiniteAggregation_hullLift_spec__1___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_hullLift___lam__0(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_hullLift___lam__0___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_hullLift___lam__1(lean_object*);
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_hullLift___lam__1___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_hullLift___lam__2(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_hullLift___lam__2___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_hullLift___lam__3(lean_object*);
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_hullLift___lam__3___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_hullLift___lam__4(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_hullLift___lam__5(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_hullLift___lam__5___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_hullLift___lam__8(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_hullLift___lam__8___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_hullLift___lam__7(lean_object*, lean_object*, lean_object*);
static const lean_closure_object lp_formal_InfiniteAggregation_hullLift___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_formal_InfiniteAggregation_hullLift___lam__0___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_formal_InfiniteAggregation_hullLift___closed__0 = (const lean_object*)&lp_formal_InfiniteAggregation_hullLift___closed__0_value;
static const lean_closure_object lp_formal_InfiniteAggregation_hullLift___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_formal_InfiniteAggregation_hullLift___lam__1___boxed, .m_arity = 1, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_formal_InfiniteAggregation_hullLift___closed__1 = (const lean_object*)&lp_formal_InfiniteAggregation_hullLift___closed__1_value;
static const lean_closure_object lp_formal_InfiniteAggregation_hullLift___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_formal_InfiniteAggregation_hullLift___lam__3___boxed, .m_arity = 1, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_formal_InfiniteAggregation_hullLift___closed__2 = (const lean_object*)&lp_formal_InfiniteAggregation_hullLift___closed__2_value;
static const lean_closure_object lp_formal_InfiniteAggregation_hullLift___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*1, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_formal_InfiniteAggregation_hullLift___lam__4, .m_arity = 3, .m_num_fixed = 1, .m_objs = {((lean_object*)&lp_formal_InfiniteAggregation_hullLift___closed__2_value)} };
static const lean_object* lp_formal_InfiniteAggregation_hullLift___closed__3 = (const lean_object*)&lp_formal_InfiniteAggregation_hullLift___closed__3_value;
static lean_once_cell_t lp_formal_InfiniteAggregation_hullLift___closed__4_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_formal_InfiniteAggregation_hullLift___closed__4;
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_hullLift(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_dotProduct___at___00InfiniteAggregation_dot_spec__0___at___00InfiniteAggregation_liftSlack_spec__0___lam__0(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_dotProduct___at___00InfiniteAggregation_dot_spec__0___at___00InfiniteAggregation_liftSlack_spec__0(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_dotProduct___at___00InfiniteAggregation_dot_spec__0___at___00InfiniteAggregation_liftSlack_spec__1___lam__0(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_dotProduct___at___00InfiniteAggregation_dot_spec__0___at___00InfiniteAggregation_liftSlack_spec__1(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_liftSlack___lam__2(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_liftSlack___lam__2___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_liftSlack(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
static lean_object* _init_lp_formal_InfiniteAggregation_liftRows___redArg___closed__0(void){
_start:
{
lean_object* v___x_1_; lean_object* v___x_2_; lean_object* v___x_3_; 
v___x_1_ = lean_unsigned_to_nat(2u);
v___x_2_ = lean_unsigned_to_nat(0u);
v___x_3_ = lean_nat_mod(v___x_2_, v___x_1_);
return v___x_3_;
}
}
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_liftRows___redArg(lean_object* v_x_4_, lean_object* v_i_5_, lean_object* v_a_6_){
_start:
{
lean_object* v___x_7_; uint8_t v___x_8_; 
v___x_7_ = lean_obj_once(&lp_formal_InfiniteAggregation_liftRows___redArg___closed__0, &lp_formal_InfiniteAggregation_liftRows___redArg___closed__0_once, _init_lp_formal_InfiniteAggregation_liftRows___redArg___closed__0);
v___x_8_ = lean_nat_dec_eq(v_i_5_, v___x_7_);
if (v___x_8_ == 0)
{
lean_object* v_snd_9_; lean_object* v___x_10_; 
v_snd_9_ = lean_ctor_get(v_x_4_, 1);
lean_inc(v_snd_9_);
lean_dec_ref(v_x_4_);
v___x_10_ = lean_apply_1(v_snd_9_, v_a_6_);
return v___x_10_;
}
else
{
lean_object* v_fst_11_; lean_object* v___x_12_; 
v_fst_11_ = lean_ctor_get(v_x_4_, 0);
lean_inc(v_fst_11_);
lean_dec_ref(v_x_4_);
v___x_12_ = lean_apply_1(v_fst_11_, v_a_6_);
return v___x_12_;
}
}
}
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_liftRows___redArg___boxed(lean_object* v_x_13_, lean_object* v_i_14_, lean_object* v_a_15_){
_start:
{
lean_object* v_res_16_; 
v_res_16_ = lp_formal_InfiniteAggregation_liftRows___redArg(v_x_13_, v_i_14_, v_a_15_);
lean_dec(v_i_14_);
return v_res_16_;
}
}
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_liftRows(lean_object* v_r_17_, lean_object* v_x_18_, lean_object* v_i_19_, lean_object* v_a_20_){
_start:
{
lean_object* v___x_21_; 
v___x_21_ = lp_formal_InfiniteAggregation_liftRows___redArg(v_x_18_, v_i_19_, v_a_20_);
return v___x_21_;
}
}
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_liftRows___boxed(lean_object* v_r_22_, lean_object* v_x_23_, lean_object* v_i_24_, lean_object* v_a_25_){
_start:
{
lean_object* v_res_26_; 
v_res_26_ = lp_formal_InfiniteAggregation_liftRows(v_r_22_, v_x_23_, v_i_24_, v_a_25_);
lean_dec(v_i_24_);
lean_dec(v_r_22_);
return v_res_26_;
}
}
LEAN_EXPORT lean_object* lp_formal_Matrix_conjTranspose___at___00InfiniteAggregation_hullLift_spec__0___redArg___lam__0(lean_object* v_x_27_){
_start:
{
lean_inc(v_x_27_);
return v_x_27_;
}
}
LEAN_EXPORT lean_object* lp_formal_Matrix_conjTranspose___at___00InfiniteAggregation_hullLift_spec__0___redArg___lam__0___boxed(lean_object* v_x_28_){
_start:
{
lean_object* v_res_29_; 
v_res_29_ = lp_formal_Matrix_conjTranspose___at___00InfiniteAggregation_hullLift_spec__0___redArg___lam__0(v_x_28_);
lean_dec(v_x_28_);
return v_res_29_;
}
}
LEAN_EXPORT lean_object* lp_formal_Matrix_conjTranspose___at___00InfiniteAggregation_hullLift_spec__0___redArg(lean_object* v_M_31_, lean_object* v_a_32_, lean_object* v_a_33_){
_start:
{
lean_object* v___f_34_; lean_object* v___x_35_; lean_object* v___x_36_; 
v___f_34_ = ((lean_object*)(lp_formal_Matrix_conjTranspose___at___00InfiniteAggregation_hullLift_spec__0___redArg___closed__0));
v___x_35_ = lean_alloc_closure((void*)(lp_mathlib_Matrix_transpose), 6, 4);
lean_closure_set(v___x_35_, 0, lean_box(0));
lean_closure_set(v___x_35_, 1, lean_box(0));
lean_closure_set(v___x_35_, 2, lean_box(0));
lean_closure_set(v___x_35_, 3, v_M_31_);
v___x_36_ = lp_mathlib_Matrix_map___redArg(v___x_35_, v___f_34_, v_a_32_, v_a_33_);
return v___x_36_;
}
}
LEAN_EXPORT lean_object* lp_formal_Matrix_conjTranspose___at___00InfiniteAggregation_hullLift_spec__0(lean_object* v_m_37_, lean_object* v_n_38_, lean_object* v_M_39_, lean_object* v_a_40_, lean_object* v_a_41_){
_start:
{
lean_object* v___x_42_; 
v___x_42_ = lp_formal_Matrix_conjTranspose___at___00InfiniteAggregation_hullLift_spec__0___redArg(v_M_39_, v_a_40_, v_a_41_);
return v___x_42_;
}
}
LEAN_EXPORT lean_object* lp_formal_Matrix_diagonal___at___00InfiniteAggregation_hullLift_spec__1___redArg___lam__0(lean_object* v_d_43_, lean_object* v_i_44_, lean_object* v_j_45_){
_start:
{
uint8_t v___x_46_; 
v___x_46_ = lean_nat_dec_eq(v_i_44_, v_j_45_);
if (v___x_46_ == 0)
{
lean_object* v___x_47_; 
lean_dec(v_i_44_);
lean_dec(v_d_43_);
v___x_47_ = lp_mathlib_Real_definition_00___x40_Mathlib_Data_Real_Basic_1850581184____hygCtx___hyg_8_;
return v___x_47_;
}
else
{
lean_object* v___x_48_; 
v___x_48_ = lean_apply_1(v_d_43_, v_i_44_);
return v___x_48_;
}
}
}
LEAN_EXPORT lean_object* lp_formal_Matrix_diagonal___at___00InfiniteAggregation_hullLift_spec__1___redArg___lam__0___boxed(lean_object* v_d_49_, lean_object* v_i_50_, lean_object* v_j_51_){
_start:
{
lean_object* v_res_52_; 
v_res_52_ = lp_formal_Matrix_diagonal___at___00InfiniteAggregation_hullLift_spec__1___redArg___lam__0(v_d_49_, v_i_50_, v_j_51_);
lean_dec(v_j_51_);
return v_res_52_;
}
}
static lean_object* _init_lp_formal_Matrix_diagonal___at___00InfiniteAggregation_hullLift_spec__1___redArg___closed__0(void){
_start:
{
lean_object* v___x_53_; 
v___x_53_ = lp_mathlib_Equiv_refl(lean_box(0));
return v___x_53_;
}
}
LEAN_EXPORT lean_object* lp_formal_Matrix_diagonal___at___00InfiniteAggregation_hullLift_spec__1___redArg(lean_object* v_d_54_, lean_object* v_a_55_, lean_object* v_a_56_){
_start:
{
lean_object* v___x_57_; lean_object* v_toFun_58_; lean_object* v___f_59_; lean_object* v___x_60_; 
v___x_57_ = lean_obj_once(&lp_formal_Matrix_diagonal___at___00InfiniteAggregation_hullLift_spec__1___redArg___closed__0, &lp_formal_Matrix_diagonal___at___00InfiniteAggregation_hullLift_spec__1___redArg___closed__0_once, _init_lp_formal_Matrix_diagonal___at___00InfiniteAggregation_hullLift_spec__1___redArg___closed__0);
v_toFun_58_ = lean_ctor_get(v___x_57_, 0);
v___f_59_ = lean_alloc_closure((void*)(lp_formal_Matrix_diagonal___at___00InfiniteAggregation_hullLift_spec__1___redArg___lam__0___boxed), 3, 1);
lean_closure_set(v___f_59_, 0, v_d_54_);
lean_inc(v_toFun_58_);
v___x_60_ = lean_apply_3(v_toFun_58_, v___f_59_, v_a_55_, v_a_56_);
return v___x_60_;
}
}
LEAN_EXPORT lean_object* lp_formal_Matrix_diagonal___at___00InfiniteAggregation_hullLift_spec__1(lean_object* v_r_61_, lean_object* v_d_62_, lean_object* v_a_63_, lean_object* v_a_64_){
_start:
{
lean_object* v___x_65_; 
v___x_65_ = lp_formal_Matrix_diagonal___at___00InfiniteAggregation_hullLift_spec__1___redArg(v_d_62_, v_a_63_, v_a_64_);
return v___x_65_;
}
}
LEAN_EXPORT lean_object* lp_formal_Matrix_diagonal___at___00InfiniteAggregation_hullLift_spec__1___boxed(lean_object* v_r_66_, lean_object* v_d_67_, lean_object* v_a_68_, lean_object* v_a_69_){
_start:
{
lean_object* v_res_70_; 
v_res_70_ = lp_formal_Matrix_diagonal___at___00InfiniteAggregation_hullLift_spec__1(v_r_66_, v_d_67_, v_a_68_, v_a_69_);
lean_dec(v_r_66_);
return v_res_70_;
}
}
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_hullLift___lam__0(lean_object* v___y_71_, lean_object* v___y_72_){
_start:
{
lean_internal_panic_unreachable();
}
}
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_hullLift___lam__0___boxed(lean_object* v___y_73_, lean_object* v___y_74_){
_start:
{
lean_object* v_res_75_; 
v_res_75_ = lp_formal_InfiniteAggregation_hullLift___lam__0(v___y_73_, v___y_74_);
lean_dec(v___y_74_);
lean_dec(v___y_73_);
return v_res_75_;
}
}
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_hullLift___lam__1(lean_object* v___y_76_){
_start:
{
lean_internal_panic_unreachable();
}
}
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_hullLift___lam__1___boxed(lean_object* v___y_77_){
_start:
{
lean_object* v_res_78_; 
v_res_78_ = lp_formal_InfiniteAggregation_hullLift___lam__1(v___y_77_);
lean_dec(v___y_77_);
return v_res_78_;
}
}
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_hullLift___lam__2(lean_object* v_00_u03c3_79_, lean_object* v___f_80_, lean_object* v___y_81_){
_start:
{
lean_object* v___x_82_; 
v___x_82_ = l_Fin_cases___redArg(v_00_u03c3_79_, v___f_80_, v___y_81_);
return v___x_82_;
}
}
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_hullLift___lam__2___boxed(lean_object* v_00_u03c3_83_, lean_object* v___f_84_, lean_object* v___y_85_){
_start:
{
lean_object* v_res_86_; 
v_res_86_ = lp_formal_InfiniteAggregation_hullLift___lam__2(v_00_u03c3_83_, v___f_84_, v___y_85_);
lean_dec(v___y_85_);
lean_dec(v_00_u03c3_83_);
return v_res_86_;
}
}
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_hullLift___lam__3(lean_object* v_x_87_){
_start:
{
lean_object* v___x_88_; 
v___x_88_ = lp_mathlib_Real_definition_00___x40_Mathlib_Data_Real_Basic_1279875089____hygCtx___hyg_8_;
return v___x_88_;
}
}
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_hullLift___lam__3___boxed(lean_object* v_x_89_){
_start:
{
lean_object* v_res_90_; 
v_res_90_ = lp_formal_InfiniteAggregation_hullLift___lam__3(v_x_89_);
lean_dec(v_x_89_);
return v_res_90_;
}
}
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_hullLift___lam__4(lean_object* v___f_91_, lean_object* v___y_92_, lean_object* v___y_93_){
_start:
{
lean_object* v___x_94_; 
v___x_94_ = lp_formal_Matrix_diagonal___at___00InfiniteAggregation_hullLift_spec__1___redArg(v___f_91_, v___y_92_, v___y_93_);
return v___x_94_;
}
}
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_hullLift___lam__5(lean_object* v___x_95_, lean_object* v___f_96_, lean_object* v___y_97_){
_start:
{
lean_object* v___x_98_; 
v___x_98_ = l_Fin_cases___redArg(v___x_95_, v___f_96_, v___y_97_);
return v___x_98_;
}
}
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_hullLift___lam__5___boxed(lean_object* v___x_99_, lean_object* v___f_100_, lean_object* v___y_101_){
_start:
{
lean_object* v_res_102_; 
v_res_102_ = lp_formal_InfiniteAggregation_hullLift___lam__5(v___x_99_, v___f_100_, v___y_101_);
lean_dec(v___y_101_);
lean_dec(v___x_99_);
return v_res_102_;
}
}
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_hullLift___lam__8(lean_object* v___f_103_, lean_object* v___f_104_, lean_object* v___y_105_, lean_object* v___y_106_){
_start:
{
lean_object* v___x_220__overap_107_; lean_object* v___x_108_; 
v___x_220__overap_107_ = l_Fin_cases___redArg(v___f_103_, v___f_104_, v___y_105_);
v___x_108_ = lean_apply_1(v___x_220__overap_107_, v___y_106_);
return v___x_108_;
}
}
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_hullLift___lam__8___boxed(lean_object* v___f_109_, lean_object* v___f_110_, lean_object* v___y_111_, lean_object* v___y_112_){
_start:
{
lean_object* v_res_113_; 
v_res_113_ = lp_formal_InfiniteAggregation_hullLift___lam__8(v___f_109_, v___f_110_, v___y_111_, v___y_112_);
lean_dec(v___y_111_);
lean_dec(v___f_109_);
return v_res_113_;
}
}
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_hullLift___lam__7(lean_object* v___x_114_, lean_object* v___y_115_, lean_object* v___y_116_){
_start:
{
lean_object* v___x_117_; 
v___x_117_ = lp_formal_Matrix_conjTranspose___at___00InfiniteAggregation_hullLift_spec__0___redArg(v___x_114_, v___y_115_, v___y_116_);
return v___x_117_;
}
}
static lean_object* _init_lp_formal_InfiniteAggregation_hullLift___closed__4(void){
_start:
{
lean_object* v___f_123_; lean_object* v___x_124_; lean_object* v___f_125_; 
v___f_123_ = ((lean_object*)(lp_formal_InfiniteAggregation_hullLift___closed__1));
v___x_124_ = lp_mathlib_Real_definition_00___x40_Mathlib_Data_Real_Basic_1279875089____hygCtx___hyg_8_;
v___f_125_ = lean_alloc_closure((void*)(lp_formal_InfiniteAggregation_hullLift___lam__5___boxed), 3, 2);
lean_closure_set(v___f_125_, 0, v___x_124_);
lean_closure_set(v___f_125_, 1, v___f_123_);
return v___f_125_;
}
}
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_hullLift(lean_object* v_r_126_, lean_object* v_x_127_, lean_object* v_00_u03c3_128_, lean_object* v_a_129_, lean_object* v_a_130_){
_start:
{
lean_object* v___x_131_; lean_object* v_toFun_132_; lean_object* v___f_133_; lean_object* v___f_134_; lean_object* v___f_135_; lean_object* v___f_136_; lean_object* v___x_137_; lean_object* v___f_138_; lean_object* v___f_139_; lean_object* v___f_140_; lean_object* v___f_141_; lean_object* v___f_142_; lean_object* v___x_143_; lean_object* v___x_144_; lean_object* v___f_145_; lean_object* v___x_146_; 
v___x_131_ = lean_obj_once(&lp_formal_Matrix_diagonal___at___00InfiniteAggregation_hullLift_spec__1___redArg___closed__0, &lp_formal_Matrix_diagonal___at___00InfiniteAggregation_hullLift_spec__1___redArg___closed__0_once, _init_lp_formal_Matrix_diagonal___at___00InfiniteAggregation_hullLift_spec__1___redArg___closed__0);
v_toFun_132_ = lean_ctor_get(v___x_131_, 0);
v___f_133_ = ((lean_object*)(lp_formal_InfiniteAggregation_hullLift___closed__0));
v___f_134_ = ((lean_object*)(lp_formal_InfiniteAggregation_hullLift___closed__1));
lean_inc(v_00_u03c3_128_);
v___f_135_ = lean_alloc_closure((void*)(lp_formal_InfiniteAggregation_hullLift___lam__2___boxed), 3, 2);
lean_closure_set(v___f_135_, 0, v_00_u03c3_128_);
lean_closure_set(v___f_135_, 1, v___f_134_);
v___f_136_ = ((lean_object*)(lp_formal_InfiniteAggregation_hullLift___closed__3));
v___x_137_ = lp_mathlib_Real_definition_00___x40_Mathlib_Data_Real_Basic_1279875089____hygCtx___hyg_8_;
v___f_138_ = lean_alloc_closure((void*)(lp_formal_InfiniteAggregation_hullLift___lam__5___boxed), 3, 2);
lean_closure_set(v___f_138_, 0, v___x_137_);
lean_closure_set(v___f_138_, 1, v___f_135_);
v___f_139_ = lean_obj_once(&lp_formal_InfiniteAggregation_hullLift___closed__4, &lp_formal_InfiniteAggregation_hullLift___closed__4_once, _init_lp_formal_InfiniteAggregation_hullLift___closed__4);
v___f_140_ = lean_alloc_closure((void*)(lp_formal_InfiniteAggregation_hullLift___lam__2___boxed), 3, 2);
lean_closure_set(v___f_140_, 0, v_00_u03c3_128_);
lean_closure_set(v___f_140_, 1, v___f_139_);
v___f_141_ = lean_alloc_closure((void*)(lp_formal_InfiniteAggregation_hullLift___lam__8___boxed), 4, 2);
lean_closure_set(v___f_141_, 0, v___f_140_);
lean_closure_set(v___f_141_, 1, v___f_133_);
v___f_142_ = lean_alloc_closure((void*)(lp_formal_InfiniteAggregation_hullLift___lam__8___boxed), 4, 2);
lean_closure_set(v___f_142_, 0, v___f_138_);
lean_closure_set(v___f_142_, 1, v___f_141_);
lean_inc(v_toFun_132_);
v___x_143_ = lean_apply_1(v_toFun_132_, v___f_142_);
v___x_144_ = lean_alloc_closure((void*)(lp_formal_InfiniteAggregation_liftRows___boxed), 4, 2);
lean_closure_set(v___x_144_, 0, v_r_126_);
lean_closure_set(v___x_144_, 1, v_x_127_);
lean_inc_ref(v___x_144_);
v___f_145_ = lean_alloc_closure((void*)(lp_formal_InfiniteAggregation_hullLift___lam__7), 3, 1);
lean_closure_set(v___f_145_, 0, v___x_144_);
v___x_146_ = lp_mathlib_Matrix_fromBlocks___redArg(v___x_143_, v___x_144_, v___f_145_, v___f_136_, v_a_129_, v_a_130_);
return v___x_146_;
}
}
LEAN_EXPORT lean_object* lp_formal_dotProduct___at___00InfiniteAggregation_dot_spec__0___at___00InfiniteAggregation_liftSlack_spec__0___lam__0(lean_object* v___x_147_, lean_object* v_i_148_){
_start:
{
lean_object* v___x_149_; lean_object* v___f_150_; 
v___x_149_ = lean_apply_1(v___x_147_, v_i_148_);
lean_inc(v___x_149_);
v___f_150_ = lean_alloc_closure((void*)(lp_mathlib_Real_definition___lam__0_00___x40_Mathlib_Data_Real_Basic_4214226450____hygCtx___hyg_8_), 3, 2);
lean_closure_set(v___f_150_, 0, v___x_149_);
lean_closure_set(v___f_150_, 1, v___x_149_);
return v___f_150_;
}
}
LEAN_EXPORT lean_object* lp_formal_dotProduct___at___00InfiniteAggregation_dot_spec__0___at___00InfiniteAggregation_liftSlack_spec__0(lean_object* v___x_151_, lean_object* v_r_152_){
_start:
{
lean_object* v___f_153_; lean_object* v___x_154_; lean_object* v___x_155_; 
v___f_153_ = lean_alloc_closure((void*)(lp_formal_dotProduct___at___00InfiniteAggregation_dot_spec__0___at___00InfiniteAggregation_liftSlack_spec__0___lam__0), 2, 1);
lean_closure_set(v___f_153_, 0, v___x_151_);
v___x_154_ = l_List_finRange(v_r_152_);
v___x_155_ = lp_mathlib_Finset_sum___at___00BoundingSieve_multSum_spec__0___redArg(v___x_154_, v___f_153_);
return v___x_155_;
}
}
LEAN_EXPORT lean_object* lp_formal_dotProduct___at___00InfiniteAggregation_dot_spec__0___at___00InfiniteAggregation_liftSlack_spec__1___lam__0(lean_object* v___x_156_, lean_object* v___x_157_, lean_object* v_i_158_){
_start:
{
lean_object* v___x_159_; lean_object* v___x_160_; lean_object* v___f_161_; 
lean_inc(v_i_158_);
v___x_159_ = lean_apply_1(v___x_156_, v_i_158_);
v___x_160_ = lean_apply_1(v___x_157_, v_i_158_);
v___f_161_ = lean_alloc_closure((void*)(lp_mathlib_Real_definition___lam__0_00___x40_Mathlib_Data_Real_Basic_4214226450____hygCtx___hyg_8_), 3, 2);
lean_closure_set(v___f_161_, 0, v___x_159_);
lean_closure_set(v___f_161_, 1, v___x_160_);
return v___f_161_;
}
}
LEAN_EXPORT lean_object* lp_formal_dotProduct___at___00InfiniteAggregation_dot_spec__0___at___00InfiniteAggregation_liftSlack_spec__1(lean_object* v___x_162_, lean_object* v___x_163_, lean_object* v_r_164_){
_start:
{
lean_object* v___f_165_; lean_object* v___x_166_; lean_object* v___x_167_; 
v___f_165_ = lean_alloc_closure((void*)(lp_formal_dotProduct___at___00InfiniteAggregation_dot_spec__0___at___00InfiniteAggregation_liftSlack_spec__1___lam__0), 3, 2);
lean_closure_set(v___f_165_, 0, v___x_162_);
lean_closure_set(v___f_165_, 1, v___x_163_);
v___x_166_ = l_List_finRange(v_r_164_);
v___x_167_ = lp_mathlib_Finset_sum___at___00BoundingSieve_multSum_spec__0___redArg(v___x_166_, v___f_165_);
return v___x_167_;
}
}
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_liftSlack___lam__2(lean_object* v___f_168_, lean_object* v___f_169_, lean_object* v___y_170_){
_start:
{
lean_object* v___x_171_; 
v___x_171_ = l_Fin_cases___redArg(v___f_168_, v___f_169_, v___y_170_);
return v___x_171_;
}
}
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_liftSlack___lam__2___boxed(lean_object* v___f_172_, lean_object* v___f_173_, lean_object* v___y_174_){
_start:
{
lean_object* v_res_175_; 
v_res_175_ = lp_formal_InfiniteAggregation_liftSlack___lam__2(v___f_172_, v___f_173_, v___y_174_);
lean_dec(v___y_174_);
lean_dec_ref(v___f_172_);
return v_res_175_;
}
}
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_liftSlack(lean_object* v_r_176_, lean_object* v_x_177_, lean_object* v_00_u03c3_178_, lean_object* v_a_179_, lean_object* v_a_180_){
_start:
{
lean_object* v_fst_181_; lean_object* v_snd_182_; lean_object* v___x_183_; lean_object* v___x_184_; lean_object* v_toFun_185_; lean_object* v___x_186_; lean_object* v___f_187_; lean_object* v___f_188_; lean_object* v___x_189_; lean_object* v___f_190_; lean_object* v___f_191_; lean_object* v___f_192_; lean_object* v___f_193_; lean_object* v___f_194_; lean_object* v___f_195_; lean_object* v___x_196_; lean_object* v___f_197_; lean_object* v___f_198_; lean_object* v___f_199_; lean_object* v___f_200_; lean_object* v___f_201_; lean_object* v___f_202_; lean_object* v___x_203_; 
v_fst_181_ = lean_ctor_get(v_x_177_, 0);
lean_inc_n(v_fst_181_, 2);
v_snd_182_ = lean_ctor_get(v_x_177_, 1);
lean_inc_n(v_snd_182_, 2);
lean_dec_ref(v_x_177_);
v___x_183_ = lean_obj_once(&lp_formal_Matrix_diagonal___at___00InfiniteAggregation_hullLift_spec__1___redArg___closed__0, &lp_formal_Matrix_diagonal___at___00InfiniteAggregation_hullLift_spec__1___redArg___closed__0_once, _init_lp_formal_Matrix_diagonal___at___00InfiniteAggregation_hullLift_spec__1___redArg___closed__0);
lean_inc_n(v_r_176_, 2);
v___x_184_ = lp_formal_dotProduct___at___00InfiniteAggregation_dot_spec__0___at___00InfiniteAggregation_liftSlack_spec__0(v_fst_181_, v_r_176_);
v_toFun_185_ = lean_ctor_get(v___x_183_, 0);
v___x_186_ = lp_mathlib_Real_definition_00___x40_Mathlib_Data_Real_Basic_1279875089____hygCtx___hyg_8_;
v___f_187_ = lean_alloc_closure((void*)(lp_mathlib_Real_definition___lam__0_00___x40_Mathlib_Data_Real_Basic_2451848184____hygCtx___hyg_8_), 2, 1);
lean_closure_set(v___f_187_, 0, v___x_184_);
v___f_188_ = lean_alloc_closure((void*)(lp_mathlib_Real_definition___lam__0_00___x40_Mathlib_Data_Real_Basic_1138242547____hygCtx___hyg_8_), 3, 2);
lean_closure_set(v___f_188_, 0, v___x_186_);
lean_closure_set(v___f_188_, 1, v___f_187_);
v___x_189_ = lp_formal_dotProduct___at___00InfiniteAggregation_dot_spec__0___at___00InfiniteAggregation_liftSlack_spec__1(v_fst_181_, v_snd_182_, v_r_176_);
v___f_190_ = ((lean_object*)(lp_formal_InfiniteAggregation_hullLift___closed__1));
v___f_191_ = ((lean_object*)(lp_formal_InfiniteAggregation_hullLift___closed__0));
v___f_192_ = lean_alloc_closure((void*)(lp_mathlib_Real_definition___lam__0_00___x40_Mathlib_Data_Real_Basic_2451848184____hygCtx___hyg_8_), 2, 1);
lean_closure_set(v___f_192_, 0, v___x_189_);
v___f_193_ = lean_alloc_closure((void*)(lp_mathlib_Real_definition___lam__0_00___x40_Mathlib_Data_Real_Basic_1138242547____hygCtx___hyg_8_), 3, 2);
lean_closure_set(v___f_193_, 0, v_00_u03c3_178_);
lean_closure_set(v___f_193_, 1, v___f_192_);
lean_inc_ref(v___f_193_);
v___f_194_ = lean_alloc_closure((void*)(lp_formal_InfiniteAggregation_liftSlack___lam__2___boxed), 3, 2);
lean_closure_set(v___f_194_, 0, v___f_193_);
lean_closure_set(v___f_194_, 1, v___f_190_);
v___f_195_ = lean_alloc_closure((void*)(lp_formal_InfiniteAggregation_liftSlack___lam__2___boxed), 3, 2);
lean_closure_set(v___f_195_, 0, v___f_188_);
lean_closure_set(v___f_195_, 1, v___f_194_);
v___x_196_ = lp_formal_dotProduct___at___00InfiniteAggregation_dot_spec__0___at___00InfiniteAggregation_liftSlack_spec__0(v_snd_182_, v_r_176_);
v___f_197_ = lean_alloc_closure((void*)(lp_mathlib_Real_definition___lam__0_00___x40_Mathlib_Data_Real_Basic_2451848184____hygCtx___hyg_8_), 2, 1);
lean_closure_set(v___f_197_, 0, v___x_196_);
v___f_198_ = lean_alloc_closure((void*)(lp_mathlib_Real_definition___lam__0_00___x40_Mathlib_Data_Real_Basic_1138242547____hygCtx___hyg_8_), 3, 2);
lean_closure_set(v___f_198_, 0, v___x_186_);
lean_closure_set(v___f_198_, 1, v___f_197_);
v___f_199_ = lean_alloc_closure((void*)(lp_formal_InfiniteAggregation_liftSlack___lam__2___boxed), 3, 2);
lean_closure_set(v___f_199_, 0, v___f_198_);
lean_closure_set(v___f_199_, 1, v___f_190_);
v___f_200_ = lean_alloc_closure((void*)(lp_formal_InfiniteAggregation_liftSlack___lam__2___boxed), 3, 2);
lean_closure_set(v___f_200_, 0, v___f_193_);
lean_closure_set(v___f_200_, 1, v___f_199_);
v___f_201_ = lean_alloc_closure((void*)(lp_formal_InfiniteAggregation_hullLift___lam__8___boxed), 4, 2);
lean_closure_set(v___f_201_, 0, v___f_200_);
lean_closure_set(v___f_201_, 1, v___f_191_);
v___f_202_ = lean_alloc_closure((void*)(lp_formal_InfiniteAggregation_hullLift___lam__8___boxed), 4, 2);
lean_closure_set(v___f_202_, 0, v___f_195_);
lean_closure_set(v___f_202_, 1, v___f_201_);
lean_inc(v_toFun_185_);
v___x_203_ = lean_apply_3(v_toFun_185_, v___f_202_, v_a_179_, v_a_180_);
return v___x_203_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_formal_Formal_InfiniteAggregation_Model(uint8_t builtin);
lean_object* initialize_formal_Formal_InfiniteAggregation_LiftSmall(uint8_t builtin);
lean_object* initialize_formal_Formal_InfiniteAggregation_HullModel(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_formal_Formal_InfiniteAggregation_Lift(uint8_t builtin) {
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
res = initialize_formal_Formal_InfiniteAggregation_LiftSmall(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_formal_Formal_InfiniteAggregation_HullModel(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
