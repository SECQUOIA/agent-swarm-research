// Lean compiler output
// Module: Formal.QuadraticAggregation.EasyDirection
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
lean_object* lp_mathlib_Nat_cast___at___00Nat_cast___at___00Nat_cast___at___00Nat_cast___at___00__private_Mathlib_NumberTheory_ModularForms_EisensteinSeries_E2_Transform_0__EisensteinSeries_00_u03b4_spec__0_spec__0_spec__2_spec__3(lean_object*);
lean_object* lp_formal_Matrix_mulVec___at___00QuadraticAggregation_q_spec__0___redArg(lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* lp_formal_dotProduct___at___00QuadraticAggregation_q_spec__1(lean_object*, lean_object*, lean_object*);
lean_object* lp_mathlib_Real_definition___lam__0_00___x40_Mathlib_Data_Real_Basic_4214226450____hygCtx___hyg_8_(lean_object*, lean_object*, lean_object*);
lean_object* lp_mathlib_Real_definition___lam__0_00___x40_Mathlib_Data_Real_Basic_1138242547____hygCtx___hyg_8_(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal___private_Formal_QuadraticAggregation_EasyDirection_0__QuadraticAggregation_matrixQuadratic___lam__0(lean_object*, lean_object*, lean_object*, lean_object*);
static lean_once_cell_t lp_formal___private_Formal_QuadraticAggregation_EasyDirection_0__QuadraticAggregation_matrixQuadratic___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_formal___private_Formal_QuadraticAggregation_EasyDirection_0__QuadraticAggregation_matrixQuadratic___closed__0;
LEAN_EXPORT lean_object* lp_formal___private_Formal_QuadraticAggregation_EasyDirection_0__QuadraticAggregation_matrixQuadratic(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal___private_Formal_QuadraticAggregation_EasyDirection_0__QuadraticAggregation_matrixQuadratic___lam__0(lean_object* v_n_1_, lean_object* v_A_2_, lean_object* v_x_3_, lean_object* v___y_4_){
_start:
{
lean_object* v___x_5_; 
v___x_5_ = lp_formal_Matrix_mulVec___at___00QuadraticAggregation_q_spec__0___redArg(v_n_1_, v_A_2_, v_x_3_, v___y_4_);
return v___x_5_;
}
}
static lean_object* _init_lp_formal___private_Formal_QuadraticAggregation_EasyDirection_0__QuadraticAggregation_matrixQuadratic___closed__0(void){
_start:
{
lean_object* v___x_6_; lean_object* v___x_7_; 
v___x_6_ = lean_unsigned_to_nat(2u);
v___x_7_ = lp_mathlib_Nat_cast___at___00Nat_cast___at___00Nat_cast___at___00Nat_cast___at___00__private_Mathlib_NumberTheory_ModularForms_EisensteinSeries_E2_Transform_0__EisensteinSeries_00_u03b4_spec__0_spec__0_spec__2_spec__3(v___x_6_);
return v___x_7_;
}
}
LEAN_EXPORT lean_object* lp_formal___private_Formal_QuadraticAggregation_EasyDirection_0__QuadraticAggregation_matrixQuadratic(lean_object* v_n_8_, lean_object* v_A_9_, lean_object* v_b_10_, lean_object* v_c_11_, lean_object* v_x_12_){
_start:
{
lean_object* v___f_13_; lean_object* v___x_14_; lean_object* v___x_15_; lean_object* v___x_16_; lean_object* v___f_17_; lean_object* v___f_18_; lean_object* v___f_19_; 
lean_inc_n(v_x_12_, 2);
lean_inc_n(v_n_8_, 2);
v___f_13_ = lean_alloc_closure((void*)(lp_formal___private_Formal_QuadraticAggregation_EasyDirection_0__QuadraticAggregation_matrixQuadratic___lam__0), 4, 3);
lean_closure_set(v___f_13_, 0, v_n_8_);
lean_closure_set(v___f_13_, 1, v_A_9_);
lean_closure_set(v___f_13_, 2, v_x_12_);
v___x_14_ = lp_formal_dotProduct___at___00QuadraticAggregation_q_spec__1(v_n_8_, v_x_12_, v___f_13_);
v___x_15_ = lean_obj_once(&lp_formal___private_Formal_QuadraticAggregation_EasyDirection_0__QuadraticAggregation_matrixQuadratic___closed__0, &lp_formal___private_Formal_QuadraticAggregation_EasyDirection_0__QuadraticAggregation_matrixQuadratic___closed__0_once, _init_lp_formal___private_Formal_QuadraticAggregation_EasyDirection_0__QuadraticAggregation_matrixQuadratic___closed__0);
v___x_16_ = lp_formal_dotProduct___at___00QuadraticAggregation_q_spec__1(v_n_8_, v_b_10_, v_x_12_);
v___f_17_ = lean_alloc_closure((void*)(lp_mathlib_Real_definition___lam__0_00___x40_Mathlib_Data_Real_Basic_4214226450____hygCtx___hyg_8_), 3, 2);
lean_closure_set(v___f_17_, 0, v___x_15_);
lean_closure_set(v___f_17_, 1, v___x_16_);
v___f_18_ = lean_alloc_closure((void*)(lp_mathlib_Real_definition___lam__0_00___x40_Mathlib_Data_Real_Basic_1138242547____hygCtx___hyg_8_), 3, 2);
lean_closure_set(v___f_18_, 0, v___x_14_);
lean_closure_set(v___f_18_, 1, v___f_17_);
v___f_19_ = lean_alloc_closure((void*)(lp_mathlib_Real_definition___lam__0_00___x40_Mathlib_Data_Real_Basic_1138242547____hygCtx___hyg_8_), 3, 2);
lean_closure_set(v___f_19_, 0, v___f_18_);
lean_closure_set(v___f_19_, 1, v_c_11_);
return v___f_19_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_formal_Formal_QuadraticAggregation_Model(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_formal_Formal_QuadraticAggregation_EasyDirection(uint8_t builtin) {
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
