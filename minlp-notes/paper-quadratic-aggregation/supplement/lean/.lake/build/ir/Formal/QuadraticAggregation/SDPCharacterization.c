// Lean compiler output
// Module: Formal.QuadraticAggregation.SDPCharacterization
// Imports: public import Init public meta import Init public import Formal.QuadraticAggregation.Headline public import Formal.DAGSpectral.UpperTriangle
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
lean_object* lp_formal_QuadraticAggregation_System_aggA___redArg(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* lp_formal_QuadraticAggregation_System_aggB___redArg(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_QuadraticAggregation_System_coefficientObjective___redArg(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_QuadraticAggregation_System_coefficientObjective(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_QuadraticAggregation_System_coefficientObjective___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal___private_Formal_QuadraticAggregation_SDPCharacterization_0__QuadraticAggregation_System_coefficientObjective_match__1_splitter___redArg(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal___private_Formal_QuadraticAggregation_SDPCharacterization_0__QuadraticAggregation_System_coefficientObjective_match__1_splitter(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal___private_Formal_QuadraticAggregation_SDPCharacterization_0__QuadraticAggregation_System_coefficientObjective_match__1_splitter___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_QuadraticAggregation_System_coefficientObjective___redArg(lean_object* v_m_1_, lean_object* v_D_2_, lean_object* v_k_3_, lean_object* v_w_4_){
_start:
{
if (lean_obj_tag(v_k_3_) == 0)
{
lean_object* v_val_5_; lean_object* v_fst_6_; lean_object* v_snd_7_; lean_object* v___x_8_; 
v_val_5_ = lean_ctor_get(v_k_3_, 0);
lean_inc(v_val_5_);
lean_dec_ref_known(v_k_3_, 1);
v_fst_6_ = lean_ctor_get(v_val_5_, 0);
lean_inc(v_fst_6_);
v_snd_7_ = lean_ctor_get(v_val_5_, 1);
lean_inc(v_snd_7_);
lean_dec(v_val_5_);
v___x_8_ = lp_formal_QuadraticAggregation_System_aggA___redArg(v_m_1_, v_D_2_, v_w_4_, v_fst_6_, v_snd_7_);
return v___x_8_;
}
else
{
lean_object* v_val_9_; lean_object* v___x_10_; 
v_val_9_ = lean_ctor_get(v_k_3_, 0);
lean_inc(v_val_9_);
lean_dec_ref_known(v_k_3_, 1);
v___x_10_ = lp_formal_QuadraticAggregation_System_aggB___redArg(v_m_1_, v_D_2_, v_w_4_, v_val_9_);
return v___x_10_;
}
}
}
LEAN_EXPORT lean_object* lp_formal_QuadraticAggregation_System_coefficientObjective(lean_object* v_n_11_, lean_object* v_m_12_, lean_object* v_D_13_, lean_object* v_k_14_, lean_object* v_w_15_){
_start:
{
lean_object* v___x_16_; 
v___x_16_ = lp_formal_QuadraticAggregation_System_coefficientObjective___redArg(v_m_12_, v_D_13_, v_k_14_, v_w_15_);
return v___x_16_;
}
}
LEAN_EXPORT lean_object* lp_formal_QuadraticAggregation_System_coefficientObjective___boxed(lean_object* v_n_17_, lean_object* v_m_18_, lean_object* v_D_19_, lean_object* v_k_20_, lean_object* v_w_21_){
_start:
{
lean_object* v_res_22_; 
v_res_22_ = lp_formal_QuadraticAggregation_System_coefficientObjective(v_n_17_, v_m_18_, v_D_19_, v_k_20_, v_w_21_);
lean_dec(v_n_17_);
return v_res_22_;
}
}
LEAN_EXPORT lean_object* lp_formal___private_Formal_QuadraticAggregation_SDPCharacterization_0__QuadraticAggregation_System_coefficientObjective_match__1_splitter___redArg(lean_object* v_k_23_, lean_object* v_h__1_24_, lean_object* v_h__2_25_){
_start:
{
if (lean_obj_tag(v_k_23_) == 0)
{
lean_object* v_val_26_; lean_object* v___x_27_; 
lean_dec(v_h__2_25_);
v_val_26_ = lean_ctor_get(v_k_23_, 0);
lean_inc(v_val_26_);
lean_dec_ref_known(v_k_23_, 1);
v___x_27_ = lean_apply_1(v_h__1_24_, v_val_26_);
return v___x_27_;
}
else
{
lean_object* v_val_28_; lean_object* v___x_29_; 
lean_dec(v_h__1_24_);
v_val_28_ = lean_ctor_get(v_k_23_, 0);
lean_inc(v_val_28_);
lean_dec_ref_known(v_k_23_, 1);
v___x_29_ = lean_apply_1(v_h__2_25_, v_val_28_);
return v___x_29_;
}
}
}
LEAN_EXPORT lean_object* lp_formal___private_Formal_QuadraticAggregation_SDPCharacterization_0__QuadraticAggregation_System_coefficientObjective_match__1_splitter(lean_object* v_n_30_, lean_object* v_motive_31_, lean_object* v_k_32_, lean_object* v_h__1_33_, lean_object* v_h__2_34_){
_start:
{
if (lean_obj_tag(v_k_32_) == 0)
{
lean_object* v_val_35_; lean_object* v___x_36_; 
lean_dec(v_h__2_34_);
v_val_35_ = lean_ctor_get(v_k_32_, 0);
lean_inc(v_val_35_);
lean_dec_ref_known(v_k_32_, 1);
v___x_36_ = lean_apply_1(v_h__1_33_, v_val_35_);
return v___x_36_;
}
else
{
lean_object* v_val_37_; lean_object* v___x_38_; 
lean_dec(v_h__1_33_);
v_val_37_ = lean_ctor_get(v_k_32_, 0);
lean_inc(v_val_37_);
lean_dec_ref_known(v_k_32_, 1);
v___x_38_ = lean_apply_1(v_h__2_34_, v_val_37_);
return v___x_38_;
}
}
}
LEAN_EXPORT lean_object* lp_formal___private_Formal_QuadraticAggregation_SDPCharacterization_0__QuadraticAggregation_System_coefficientObjective_match__1_splitter___boxed(lean_object* v_n_39_, lean_object* v_motive_40_, lean_object* v_k_41_, lean_object* v_h__1_42_, lean_object* v_h__2_43_){
_start:
{
lean_object* v_res_44_; 
v_res_44_ = lp_formal___private_Formal_QuadraticAggregation_SDPCharacterization_0__QuadraticAggregation_System_coefficientObjective_match__1_splitter(v_n_39_, v_motive_40_, v_k_41_, v_h__1_42_, v_h__2_43_);
lean_dec(v_n_39_);
return v_res_44_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_formal_Formal_QuadraticAggregation_Headline(uint8_t builtin);
lean_object* initialize_formal_Formal_DAGSpectral_UpperTriangle(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_formal_Formal_QuadraticAggregation_SDPCharacterization(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_formal_Formal_QuadraticAggregation_Headline(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_formal_Formal_DAGSpectral_UpperTriangle(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
