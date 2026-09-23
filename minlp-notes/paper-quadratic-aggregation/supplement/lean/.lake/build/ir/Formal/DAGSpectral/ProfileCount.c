// Lean compiler output
// Module: Formal.DAGSpectral.ProfileCount
// Imports: public import Init public meta import Init public import Formal.DAGSpectral.Rounding public import Mathlib.Data.Fintype.BigOperators public import Mathlib.Algebra.BigOperators.Ring.Finset public import Mathlib.Data.Finset.Pi
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
lean_object* lp_mathlib_Multiset_attach___redArg(lean_object*);
lean_object* l_instDecidableEqFin___boxed(lean_object*, lean_object*, lean_object*);
lean_object* l_List_finRange(lean_object*);
lean_object* lp_mathlib_Fintype_piFinset___redArg(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_DAGSpectral_instFintypeBoundedProfile___aux__1___lam__0(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_DAGSpectral_instFintypeBoundedProfile___aux__1___lam__0___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_DAGSpectral_instFintypeBoundedProfile___aux__1(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_DAGSpectral_instFintypeBoundedProfile(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_DAGSpectral_instFintypeBoundedProfile___aux__1___lam__0(lean_object* v_s_1_, lean_object* v_x_2_){
_start:
{
lean_object* v___x_3_; 
v___x_3_ = lp_mathlib_Multiset_attach___redArg(v_s_1_);
return v___x_3_;
}
}
LEAN_EXPORT lean_object* lp_formal_DAGSpectral_instFintypeBoundedProfile___aux__1___lam__0___boxed(lean_object* v_s_4_, lean_object* v_x_5_){
_start:
{
lean_object* v_res_6_; 
v_res_6_ = lp_formal_DAGSpectral_instFintypeBoundedProfile___aux__1___lam__0(v_s_4_, v_x_5_);
lean_dec(v_x_5_);
return v_res_6_;
}
}
LEAN_EXPORT lean_object* lp_formal_DAGSpectral_instFintypeBoundedProfile___aux__1(lean_object* v_d_7_, lean_object* v_s_8_){
_start:
{
lean_object* v___f_9_; lean_object* v___x_10_; lean_object* v___x_11_; lean_object* v___x_12_; 
v___f_9_ = lean_alloc_closure((void*)(lp_formal_DAGSpectral_instFintypeBoundedProfile___aux__1___lam__0___boxed), 2, 1);
lean_closure_set(v___f_9_, 0, v_s_8_);
lean_inc(v_d_7_);
v___x_10_ = lean_alloc_closure((void*)(l_instDecidableEqFin___boxed), 3, 1);
lean_closure_set(v___x_10_, 0, v_d_7_);
v___x_11_ = l_List_finRange(v_d_7_);
v___x_12_ = lp_mathlib_Fintype_piFinset___redArg(v___x_10_, v___x_11_, v___f_9_);
return v___x_12_;
}
}
LEAN_EXPORT lean_object* lp_formal_DAGSpectral_instFintypeBoundedProfile(lean_object* v_d_13_, lean_object* v_s_14_){
_start:
{
lean_object* v___f_15_; lean_object* v___x_16_; lean_object* v___x_17_; lean_object* v___x_18_; 
v___f_15_ = lean_alloc_closure((void*)(lp_formal_DAGSpectral_instFintypeBoundedProfile___aux__1___lam__0___boxed), 2, 1);
lean_closure_set(v___f_15_, 0, v_s_14_);
lean_inc(v_d_13_);
v___x_16_ = lean_alloc_closure((void*)(l_instDecidableEqFin___boxed), 3, 1);
lean_closure_set(v___x_16_, 0, v_d_13_);
v___x_17_ = l_List_finRange(v_d_13_);
v___x_18_ = lp_mathlib_Fintype_piFinset___redArg(v___x_16_, v___x_17_, v___f_15_);
return v___x_18_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_formal_Formal_DAGSpectral_Rounding(uint8_t builtin);
lean_object* initialize_mathlib_Mathlib_Data_Fintype_BigOperators(uint8_t builtin);
lean_object* initialize_mathlib_Mathlib_Algebra_BigOperators_Ring_Finset(uint8_t builtin);
lean_object* initialize_mathlib_Mathlib_Data_Finset_Pi(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_formal_Formal_DAGSpectral_ProfileCount(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_formal_Formal_DAGSpectral_Rounding(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_mathlib_Mathlib_Data_Fintype_BigOperators(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_mathlib_Mathlib_Algebra_BigOperators_Ring_Finset(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_mathlib_Mathlib_Data_Finset_Pi(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
