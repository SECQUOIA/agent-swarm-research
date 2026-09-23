// Lean compiler output
// Module: Formal.QuadraticAggregation.ShorBlock
// Imports: public import Init public meta import Init public import Formal.QuadraticAggregation.Model
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
extern lean_object* lp_mathlib_Real_definition_00___x40_Mathlib_Data_Real_Basic_1279875089____hygCtx___hyg_8_;
lean_object* lp_mathlib_Equiv_refl(lean_object*);
lean_object* lp_mathlib_Real_definition___lam__0_00___x40_Mathlib_Data_Real_Basic_4214226450____hygCtx___hyg_8_(lean_object*, lean_object*, lean_object*);
lean_object* lp_mathlib_Matrix_fromBlocks___redArg(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_QuadraticAggregation_outer___redArg___lam__0(lean_object*, lean_object*, lean_object*);
static lean_once_cell_t lp_formal_QuadraticAggregation_outer___redArg___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_formal_QuadraticAggregation_outer___redArg___closed__0;
LEAN_EXPORT lean_object* lp_formal_QuadraticAggregation_outer___redArg(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_QuadraticAggregation_outer(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_QuadraticAggregation_outer___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_Matrix_diagonal___at___00QuadraticAggregation_shorBlock_spec__0___lam__0(lean_object*, lean_object*, lean_object*);
static lean_once_cell_t lp_formal_Matrix_diagonal___at___00QuadraticAggregation_shorBlock_spec__0___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_formal_Matrix_diagonal___at___00QuadraticAggregation_shorBlock_spec__0___closed__0;
LEAN_EXPORT lean_object* lp_formal_Matrix_diagonal___at___00QuadraticAggregation_shorBlock_spec__0(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_QuadraticAggregation_shorBlock___redArg___lam__0(lean_object*);
LEAN_EXPORT lean_object* lp_formal_QuadraticAggregation_shorBlock___redArg___lam__1(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_QuadraticAggregation_shorBlock___redArg___lam__2(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_QuadraticAggregation_shorBlock___redArg___lam__3(lean_object*, lean_object*, lean_object*);
static lean_once_cell_t lp_formal_QuadraticAggregation_shorBlock___redArg___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_formal_QuadraticAggregation_shorBlock___redArg___closed__0;
static const lean_closure_object lp_formal_QuadraticAggregation_shorBlock___redArg___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_formal_QuadraticAggregation_shorBlock___redArg___lam__0, .m_arity = 1, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_formal_QuadraticAggregation_shorBlock___redArg___closed__1 = (const lean_object*)&lp_formal_QuadraticAggregation_shorBlock___redArg___closed__1_value;
static const lean_closure_object lp_formal_QuadraticAggregation_shorBlock___redArg___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*1, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_formal_QuadraticAggregation_shorBlock___redArg___lam__3, .m_arity = 3, .m_num_fixed = 1, .m_objs = {((lean_object*)&lp_formal_QuadraticAggregation_shorBlock___redArg___closed__1_value)} };
static const lean_object* lp_formal_QuadraticAggregation_shorBlock___redArg___closed__2 = (const lean_object*)&lp_formal_QuadraticAggregation_shorBlock___redArg___closed__2_value;
LEAN_EXPORT lean_object* lp_formal_QuadraticAggregation_shorBlock___redArg(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_QuadraticAggregation_shorBlock(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_QuadraticAggregation_shorBlock___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_QuadraticAggregation_outer___redArg___lam__0(lean_object* v_x_1_, lean_object* v_i_2_, lean_object* v_j_3_){
_start:
{
lean_object* v___x_4_; lean_object* v___x_5_; lean_object* v___f_6_; 
lean_inc(v_x_1_);
v___x_4_ = lean_apply_1(v_x_1_, v_i_2_);
v___x_5_ = lean_apply_1(v_x_1_, v_j_3_);
v___f_6_ = lean_alloc_closure((void*)(lp_mathlib_Real_definition___lam__0_00___x40_Mathlib_Data_Real_Basic_4214226450____hygCtx___hyg_8_), 3, 2);
lean_closure_set(v___f_6_, 0, v___x_4_);
lean_closure_set(v___f_6_, 1, v___x_5_);
return v___f_6_;
}
}
static lean_object* _init_lp_formal_QuadraticAggregation_outer___redArg___closed__0(void){
_start:
{
lean_object* v___x_7_; 
v___x_7_ = lp_mathlib_Equiv_refl(lean_box(0));
return v___x_7_;
}
}
LEAN_EXPORT lean_object* lp_formal_QuadraticAggregation_outer___redArg(lean_object* v_x_8_, lean_object* v_a_9_, lean_object* v_a_10_){
_start:
{
lean_object* v___x_11_; lean_object* v_toFun_12_; lean_object* v___f_13_; lean_object* v___x_14_; 
v___x_11_ = lean_obj_once(&lp_formal_QuadraticAggregation_outer___redArg___closed__0, &lp_formal_QuadraticAggregation_outer___redArg___closed__0_once, _init_lp_formal_QuadraticAggregation_outer___redArg___closed__0);
v_toFun_12_ = lean_ctor_get(v___x_11_, 0);
v___f_13_ = lean_alloc_closure((void*)(lp_formal_QuadraticAggregation_outer___redArg___lam__0), 3, 1);
lean_closure_set(v___f_13_, 0, v_x_8_);
lean_inc(v_toFun_12_);
v___x_14_ = lean_apply_3(v_toFun_12_, v___f_13_, v_a_9_, v_a_10_);
return v___x_14_;
}
}
LEAN_EXPORT lean_object* lp_formal_QuadraticAggregation_outer(lean_object* v_n_15_, lean_object* v_x_16_, lean_object* v_a_17_, lean_object* v_a_18_){
_start:
{
lean_object* v___x_19_; 
v___x_19_ = lp_formal_QuadraticAggregation_outer___redArg(v_x_16_, v_a_17_, v_a_18_);
return v___x_19_;
}
}
LEAN_EXPORT lean_object* lp_formal_QuadraticAggregation_outer___boxed(lean_object* v_n_20_, lean_object* v_x_21_, lean_object* v_a_22_, lean_object* v_a_23_){
_start:
{
lean_object* v_res_24_; 
v_res_24_ = lp_formal_QuadraticAggregation_outer(v_n_20_, v_x_21_, v_a_22_, v_a_23_);
lean_dec(v_n_20_);
return v_res_24_;
}
}
LEAN_EXPORT lean_object* lp_formal_Matrix_diagonal___at___00QuadraticAggregation_shorBlock_spec__0___lam__0(lean_object* v_d_25_, lean_object* v_i_26_, lean_object* v_j_27_){
_start:
{
lean_object* v___x_28_; 
v___x_28_ = lean_apply_1(v_d_25_, v_i_26_);
return v___x_28_;
}
}
static lean_object* _init_lp_formal_Matrix_diagonal___at___00QuadraticAggregation_shorBlock_spec__0___closed__0(void){
_start:
{
lean_object* v___x_29_; 
v___x_29_ = lp_mathlib_Equiv_refl(lean_box(0));
return v___x_29_;
}
}
LEAN_EXPORT lean_object* lp_formal_Matrix_diagonal___at___00QuadraticAggregation_shorBlock_spec__0(lean_object* v_d_30_, lean_object* v_a_31_, lean_object* v_a_32_){
_start:
{
lean_object* v___x_33_; lean_object* v_toFun_34_; lean_object* v___f_35_; lean_object* v___x_36_; 
v___x_33_ = lean_obj_once(&lp_formal_Matrix_diagonal___at___00QuadraticAggregation_shorBlock_spec__0___closed__0, &lp_formal_Matrix_diagonal___at___00QuadraticAggregation_shorBlock_spec__0___closed__0_once, _init_lp_formal_Matrix_diagonal___at___00QuadraticAggregation_shorBlock_spec__0___closed__0);
v_toFun_34_ = lean_ctor_get(v___x_33_, 0);
v___f_35_ = lean_alloc_closure((void*)(lp_formal_Matrix_diagonal___at___00QuadraticAggregation_shorBlock_spec__0___lam__0), 3, 1);
lean_closure_set(v___f_35_, 0, v_d_30_);
lean_inc(v_toFun_34_);
v___x_36_ = lean_apply_3(v_toFun_34_, v___f_35_, v_a_31_, v_a_32_);
return v___x_36_;
}
}
LEAN_EXPORT lean_object* lp_formal_QuadraticAggregation_shorBlock___redArg___lam__0(lean_object* v_x_37_){
_start:
{
lean_object* v___x_38_; 
v___x_38_ = lp_mathlib_Real_definition_00___x40_Mathlib_Data_Real_Basic_1279875089____hygCtx___hyg_8_;
return v___x_38_;
}
}
LEAN_EXPORT lean_object* lp_formal_QuadraticAggregation_shorBlock___redArg___lam__1(lean_object* v_x_39_, lean_object* v_x_40_, lean_object* v_j_41_){
_start:
{
lean_object* v___x_42_; 
v___x_42_ = lean_apply_1(v_x_39_, v_j_41_);
return v___x_42_;
}
}
LEAN_EXPORT lean_object* lp_formal_QuadraticAggregation_shorBlock___redArg___lam__2(lean_object* v_x_43_, lean_object* v_i_44_, lean_object* v_x_45_){
_start:
{
lean_object* v___x_46_; 
v___x_46_ = lean_apply_1(v_x_43_, v_i_44_);
return v___x_46_;
}
}
LEAN_EXPORT lean_object* lp_formal_QuadraticAggregation_shorBlock___redArg___lam__3(lean_object* v___f_47_, lean_object* v___y_48_, lean_object* v___y_49_){
_start:
{
lean_object* v___x_50_; 
v___x_50_ = lp_formal_Matrix_diagonal___at___00QuadraticAggregation_shorBlock_spec__0(v___f_47_, v___y_48_, v___y_49_);
return v___x_50_;
}
}
static lean_object* _init_lp_formal_QuadraticAggregation_shorBlock___redArg___closed__0(void){
_start:
{
lean_object* v___x_51_; 
v___x_51_ = lp_mathlib_Equiv_refl(lean_box(0));
return v___x_51_;
}
}
LEAN_EXPORT lean_object* lp_formal_QuadraticAggregation_shorBlock___redArg(lean_object* v_x_55_, lean_object* v_X_56_, lean_object* v_a_57_, lean_object* v_a_58_){
_start:
{
lean_object* v___x_59_; lean_object* v_toFun_60_; lean_object* v_toFun_61_; lean_object* v___f_62_; lean_object* v___f_63_; lean_object* v___f_64_; lean_object* v___x_65_; lean_object* v___x_66_; lean_object* v___x_67_; 
v___x_59_ = lean_obj_once(&lp_formal_QuadraticAggregation_shorBlock___redArg___closed__0, &lp_formal_QuadraticAggregation_shorBlock___redArg___closed__0_once, _init_lp_formal_QuadraticAggregation_shorBlock___redArg___closed__0);
v_toFun_60_ = lean_ctor_get(v___x_59_, 0);
v_toFun_61_ = lean_ctor_get(v___x_59_, 0);
lean_inc(v_x_55_);
v___f_62_ = lean_alloc_closure((void*)(lp_formal_QuadraticAggregation_shorBlock___redArg___lam__1), 3, 1);
lean_closure_set(v___f_62_, 0, v_x_55_);
v___f_63_ = lean_alloc_closure((void*)(lp_formal_QuadraticAggregation_shorBlock___redArg___lam__2), 3, 1);
lean_closure_set(v___f_63_, 0, v_x_55_);
v___f_64_ = ((lean_object*)(lp_formal_QuadraticAggregation_shorBlock___redArg___closed__2));
lean_inc(v_toFun_60_);
v___x_65_ = lean_apply_1(v_toFun_60_, v___f_62_);
lean_inc(v_toFun_61_);
v___x_66_ = lean_apply_1(v_toFun_61_, v___f_63_);
v___x_67_ = lp_mathlib_Matrix_fromBlocks___redArg(v___f_64_, v___x_65_, v___x_66_, v_X_56_, v_a_57_, v_a_58_);
return v___x_67_;
}
}
LEAN_EXPORT lean_object* lp_formal_QuadraticAggregation_shorBlock(lean_object* v_n_68_, lean_object* v_x_69_, lean_object* v_X_70_, lean_object* v_a_71_, lean_object* v_a_72_){
_start:
{
lean_object* v___x_73_; 
v___x_73_ = lp_formal_QuadraticAggregation_shorBlock___redArg(v_x_69_, v_X_70_, v_a_71_, v_a_72_);
return v___x_73_;
}
}
LEAN_EXPORT lean_object* lp_formal_QuadraticAggregation_shorBlock___boxed(lean_object* v_n_74_, lean_object* v_x_75_, lean_object* v_X_76_, lean_object* v_a_77_, lean_object* v_a_78_){
_start:
{
lean_object* v_res_79_; 
v_res_79_ = lp_formal_QuadraticAggregation_shorBlock(v_n_74_, v_x_75_, v_X_76_, v_a_77_, v_a_78_);
lean_dec(v_n_74_);
return v_res_79_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_formal_Formal_QuadraticAggregation_Model(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_formal_Formal_QuadraticAggregation_ShorBlock(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_formal_Formal_QuadraticAggregation_Model(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
