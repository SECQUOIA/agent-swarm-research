// Lean compiler output
// Module: Formal.DAGSpectral.UpperTriangle
// Imports: public import Init public meta import Init public import Formal.DAGSpectral.ProfileCount public import Mathlib.Algebra.BigOperators.Fin
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
lean_object* lean_nat_add(lean_object*, lean_object*);
lean_object* l_List_finRange(lean_object*);
lean_object* lp_mathlib_Finset_sigma___redArg(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_DAGSpectral_instFintypeUpperCoord___aux__1___lam__0(lean_object*);
LEAN_EXPORT lean_object* lp_formal_DAGSpectral_instFintypeUpperCoord___aux__1___lam__0___boxed(lean_object*);
static const lean_closure_object lp_formal_DAGSpectral_instFintypeUpperCoord___aux__1___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_formal_DAGSpectral_instFintypeUpperCoord___aux__1___lam__0___boxed, .m_arity = 1, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_formal_DAGSpectral_instFintypeUpperCoord___aux__1___closed__0 = (const lean_object*)&lp_formal_DAGSpectral_instFintypeUpperCoord___aux__1___closed__0_value;
LEAN_EXPORT lean_object* lp_formal_DAGSpectral_instFintypeUpperCoord___aux__1(lean_object*);
LEAN_EXPORT lean_object* lp_formal_DAGSpectral_instFintypeUpperCoord(lean_object*);
LEAN_EXPORT lean_object* lp_formal_DAGSpectral_upperCoordEquiv___lam__0(lean_object*);
LEAN_EXPORT lean_object* lp_formal_DAGSpectral_upperCoordEquiv___lam__1(lean_object*);
static const lean_closure_object lp_formal_DAGSpectral_upperCoordEquiv___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_formal_DAGSpectral_upperCoordEquiv___lam__0, .m_arity = 1, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_formal_DAGSpectral_upperCoordEquiv___closed__0 = (const lean_object*)&lp_formal_DAGSpectral_upperCoordEquiv___closed__0_value;
static const lean_closure_object lp_formal_DAGSpectral_upperCoordEquiv___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_formal_DAGSpectral_upperCoordEquiv___lam__1, .m_arity = 1, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_formal_DAGSpectral_upperCoordEquiv___closed__1 = (const lean_object*)&lp_formal_DAGSpectral_upperCoordEquiv___closed__1_value;
static const lean_ctor_object lp_formal_DAGSpectral_upperCoordEquiv___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 0}, .m_objs = {((lean_object*)&lp_formal_DAGSpectral_upperCoordEquiv___closed__0_value),((lean_object*)&lp_formal_DAGSpectral_upperCoordEquiv___closed__1_value)}};
static const lean_object* lp_formal_DAGSpectral_upperCoordEquiv___closed__2 = (const lean_object*)&lp_formal_DAGSpectral_upperCoordEquiv___closed__2_value;
LEAN_EXPORT lean_object* lp_formal_DAGSpectral_upperCoordEquiv(lean_object*);
LEAN_EXPORT lean_object* lp_formal_DAGSpectral_upperCoordEquiv___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_formal_DAGSpectral_instFintypeUpperCoord___aux__1___lam__0(lean_object* v_x_1_){
_start:
{
lean_object* v___x_2_; lean_object* v___x_3_; lean_object* v___x_4_; 
v___x_2_ = lean_unsigned_to_nat(1u);
v___x_3_ = lean_nat_add(v_x_1_, v___x_2_);
v___x_4_ = l_List_finRange(v___x_3_);
return v___x_4_;
}
}
LEAN_EXPORT lean_object* lp_formal_DAGSpectral_instFintypeUpperCoord___aux__1___lam__0___boxed(lean_object* v_x_5_){
_start:
{
lean_object* v_res_6_; 
v_res_6_ = lp_formal_DAGSpectral_instFintypeUpperCoord___aux__1___lam__0(v_x_5_);
lean_dec(v_x_5_);
return v_res_6_;
}
}
LEAN_EXPORT lean_object* lp_formal_DAGSpectral_instFintypeUpperCoord___aux__1(lean_object* v_r_8_){
_start:
{
lean_object* v___f_9_; lean_object* v___x_10_; lean_object* v___x_11_; 
v___f_9_ = ((lean_object*)(lp_formal_DAGSpectral_instFintypeUpperCoord___aux__1___closed__0));
v___x_10_ = l_List_finRange(v_r_8_);
v___x_11_ = lp_mathlib_Finset_sigma___redArg(v___x_10_, v___f_9_);
return v___x_11_;
}
}
LEAN_EXPORT lean_object* lp_formal_DAGSpectral_instFintypeUpperCoord(lean_object* v_r_12_){
_start:
{
lean_object* v___f_13_; lean_object* v___x_14_; lean_object* v___x_15_; 
v___f_13_ = ((lean_object*)(lp_formal_DAGSpectral_instFintypeUpperCoord___aux__1___closed__0));
v___x_14_ = l_List_finRange(v_r_12_);
v___x_15_ = lp_mathlib_Finset_sigma___redArg(v___x_14_, v___f_13_);
return v___x_15_;
}
}
LEAN_EXPORT lean_object* lp_formal_DAGSpectral_upperCoordEquiv___lam__0(lean_object* v_z_16_){
_start:
{
lean_object* v_fst_17_; lean_object* v_snd_18_; lean_object* v___x_20_; uint8_t v_isShared_21_; uint8_t v_isSharedCheck_25_; 
v_fst_17_ = lean_ctor_get(v_z_16_, 0);
v_snd_18_ = lean_ctor_get(v_z_16_, 1);
v_isSharedCheck_25_ = !lean_is_exclusive(v_z_16_);
if (v_isSharedCheck_25_ == 0)
{
v___x_20_ = v_z_16_;
v_isShared_21_ = v_isSharedCheck_25_;
goto v_resetjp_19_;
}
else
{
lean_inc(v_snd_18_);
lean_inc(v_fst_17_);
lean_dec(v_z_16_);
v___x_20_ = lean_box(0);
v_isShared_21_ = v_isSharedCheck_25_;
goto v_resetjp_19_;
}
v_resetjp_19_:
{
lean_object* v___x_23_; 
if (v_isShared_21_ == 0)
{
lean_ctor_set(v___x_20_, 1, v_fst_17_);
lean_ctor_set(v___x_20_, 0, v_snd_18_);
v___x_23_ = v___x_20_;
goto v_reusejp_22_;
}
else
{
lean_object* v_reuseFailAlloc_24_; 
v_reuseFailAlloc_24_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_24_, 0, v_snd_18_);
lean_ctor_set(v_reuseFailAlloc_24_, 1, v_fst_17_);
v___x_23_ = v_reuseFailAlloc_24_;
goto v_reusejp_22_;
}
v_reusejp_22_:
{
return v___x_23_;
}
}
}
}
LEAN_EXPORT lean_object* lp_formal_DAGSpectral_upperCoordEquiv___lam__1(lean_object* v_z_26_){
_start:
{
lean_object* v_fst_27_; lean_object* v_snd_28_; lean_object* v___x_30_; uint8_t v_isShared_31_; uint8_t v_isSharedCheck_35_; 
v_fst_27_ = lean_ctor_get(v_z_26_, 0);
v_snd_28_ = lean_ctor_get(v_z_26_, 1);
v_isSharedCheck_35_ = !lean_is_exclusive(v_z_26_);
if (v_isSharedCheck_35_ == 0)
{
v___x_30_ = v_z_26_;
v_isShared_31_ = v_isSharedCheck_35_;
goto v_resetjp_29_;
}
else
{
lean_inc(v_snd_28_);
lean_inc(v_fst_27_);
lean_dec(v_z_26_);
v___x_30_ = lean_box(0);
v_isShared_31_ = v_isSharedCheck_35_;
goto v_resetjp_29_;
}
v_resetjp_29_:
{
lean_object* v___x_33_; 
if (v_isShared_31_ == 0)
{
lean_ctor_set(v___x_30_, 1, v_fst_27_);
lean_ctor_set(v___x_30_, 0, v_snd_28_);
v___x_33_ = v___x_30_;
goto v_reusejp_32_;
}
else
{
lean_object* v_reuseFailAlloc_34_; 
v_reuseFailAlloc_34_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_34_, 0, v_snd_28_);
lean_ctor_set(v_reuseFailAlloc_34_, 1, v_fst_27_);
v___x_33_ = v_reuseFailAlloc_34_;
goto v_reusejp_32_;
}
v_reusejp_32_:
{
return v___x_33_;
}
}
}
}
LEAN_EXPORT lean_object* lp_formal_DAGSpectral_upperCoordEquiv(lean_object* v_r_41_){
_start:
{
lean_object* v___x_42_; 
v___x_42_ = ((lean_object*)(lp_formal_DAGSpectral_upperCoordEquiv___closed__2));
return v___x_42_;
}
}
LEAN_EXPORT lean_object* lp_formal_DAGSpectral_upperCoordEquiv___boxed(lean_object* v_r_43_){
_start:
{
lean_object* v_res_44_; 
v_res_44_ = lp_formal_DAGSpectral_upperCoordEquiv(v_r_43_);
lean_dec(v_r_43_);
return v_res_44_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_formal_Formal_DAGSpectral_ProfileCount(uint8_t builtin);
lean_object* initialize_mathlib_Mathlib_Algebra_BigOperators_Fin(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_formal_Formal_DAGSpectral_UpperTriangle(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_formal_Formal_DAGSpectral_ProfileCount(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_mathlib_Mathlib_Algebra_BigOperators_Fin(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
