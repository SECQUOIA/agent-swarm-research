// Lean compiler output
// Module: Formal.InfiniteAggregation.Good
// Imports: public import Init public meta import Init public import Formal.InfiniteAggregation.GoodSpectral public import Formal.InfiniteAggregation.GoodConvex
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
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_homogeneousCoordinates___redArg(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_homogeneousCoordinates(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_homogeneousCoordinates___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal___private_Formal_InfiniteAggregation_Good_0__InfiniteAggregation_homogeneousCoordinates_match__1_splitter___redArg(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal___private_Formal_InfiniteAggregation_Good_0__InfiniteAggregation_homogeneousCoordinates_match__1_splitter(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal___private_Formal_InfiniteAggregation_Good_0__InfiniteAggregation_homogeneousCoordinates_match__1_splitter___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_homogeneousCoordinates___redArg(lean_object* v_z_1_, lean_object* v_x_2_){
_start:
{
if (lean_obj_tag(v_x_2_) == 0)
{
lean_object* v_snd_3_; 
v_snd_3_ = lean_ctor_get(v_z_1_, 1);
lean_inc(v_snd_3_);
lean_dec_ref(v_z_1_);
return v_snd_3_;
}
else
{
lean_object* v_val_4_; 
v_val_4_ = lean_ctor_get(v_x_2_, 0);
lean_inc(v_val_4_);
lean_dec_ref_known(v_x_2_, 1);
if (lean_obj_tag(v_val_4_) == 0)
{
lean_object* v_fst_5_; lean_object* v_val_6_; lean_object* v_fst_7_; lean_object* v___x_8_; 
v_fst_5_ = lean_ctor_get(v_z_1_, 0);
lean_inc(v_fst_5_);
lean_dec_ref(v_z_1_);
v_val_6_ = lean_ctor_get(v_val_4_, 0);
lean_inc(v_val_6_);
lean_dec_ref_known(v_val_4_, 1);
v_fst_7_ = lean_ctor_get(v_fst_5_, 0);
lean_inc(v_fst_7_);
lean_dec(v_fst_5_);
v___x_8_ = lean_apply_1(v_fst_7_, v_val_6_);
return v___x_8_;
}
else
{
lean_object* v_fst_9_; lean_object* v_val_10_; lean_object* v_snd_11_; lean_object* v___x_12_; 
v_fst_9_ = lean_ctor_get(v_z_1_, 0);
lean_inc(v_fst_9_);
lean_dec_ref(v_z_1_);
v_val_10_ = lean_ctor_get(v_val_4_, 0);
lean_inc(v_val_10_);
lean_dec_ref_known(v_val_4_, 1);
v_snd_11_ = lean_ctor_get(v_fst_9_, 1);
lean_inc(v_snd_11_);
lean_dec(v_fst_9_);
v___x_12_ = lean_apply_1(v_snd_11_, v_val_10_);
return v___x_12_;
}
}
}
}
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_homogeneousCoordinates(lean_object* v_r_13_, lean_object* v_z_14_, lean_object* v_x_15_){
_start:
{
lean_object* v___x_16_; 
v___x_16_ = lp_formal_InfiniteAggregation_homogeneousCoordinates___redArg(v_z_14_, v_x_15_);
return v___x_16_;
}
}
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_homogeneousCoordinates___boxed(lean_object* v_r_17_, lean_object* v_z_18_, lean_object* v_x_19_){
_start:
{
lean_object* v_res_20_; 
v_res_20_ = lp_formal_InfiniteAggregation_homogeneousCoordinates(v_r_17_, v_z_18_, v_x_19_);
lean_dec(v_r_17_);
return v_res_20_;
}
}
LEAN_EXPORT lean_object* lp_formal___private_Formal_InfiniteAggregation_Good_0__InfiniteAggregation_homogeneousCoordinates_match__1_splitter___redArg(lean_object* v_x_21_, lean_object* v_h__1_22_, lean_object* v_h__2_23_, lean_object* v_h__3_24_){
_start:
{
if (lean_obj_tag(v_x_21_) == 0)
{
lean_object* v___x_25_; lean_object* v___x_26_; 
lean_dec(v_h__3_24_);
lean_dec(v_h__2_23_);
v___x_25_ = lean_box(0);
v___x_26_ = lean_apply_1(v_h__1_22_, v___x_25_);
return v___x_26_;
}
else
{
lean_object* v_val_27_; 
lean_dec(v_h__1_22_);
v_val_27_ = lean_ctor_get(v_x_21_, 0);
lean_inc(v_val_27_);
lean_dec_ref_known(v_x_21_, 1);
if (lean_obj_tag(v_val_27_) == 0)
{
lean_object* v_val_28_; lean_object* v___x_29_; 
lean_dec(v_h__3_24_);
v_val_28_ = lean_ctor_get(v_val_27_, 0);
lean_inc(v_val_28_);
lean_dec_ref_known(v_val_27_, 1);
v___x_29_ = lean_apply_1(v_h__2_23_, v_val_28_);
return v___x_29_;
}
else
{
lean_object* v_val_30_; lean_object* v___x_31_; 
lean_dec(v_h__2_23_);
v_val_30_ = lean_ctor_get(v_val_27_, 0);
lean_inc(v_val_30_);
lean_dec_ref_known(v_val_27_, 1);
v___x_31_ = lean_apply_1(v_h__3_24_, v_val_30_);
return v___x_31_;
}
}
}
}
LEAN_EXPORT lean_object* lp_formal___private_Formal_InfiniteAggregation_Good_0__InfiniteAggregation_homogeneousCoordinates_match__1_splitter(lean_object* v_r_32_, lean_object* v_motive_33_, lean_object* v_x_34_, lean_object* v_h__1_35_, lean_object* v_h__2_36_, lean_object* v_h__3_37_){
_start:
{
if (lean_obj_tag(v_x_34_) == 0)
{
lean_object* v___x_38_; lean_object* v___x_39_; 
lean_dec(v_h__3_37_);
lean_dec(v_h__2_36_);
v___x_38_ = lean_box(0);
v___x_39_ = lean_apply_1(v_h__1_35_, v___x_38_);
return v___x_39_;
}
else
{
lean_object* v_val_40_; 
lean_dec(v_h__1_35_);
v_val_40_ = lean_ctor_get(v_x_34_, 0);
lean_inc(v_val_40_);
lean_dec_ref_known(v_x_34_, 1);
if (lean_obj_tag(v_val_40_) == 0)
{
lean_object* v_val_41_; lean_object* v___x_42_; 
lean_dec(v_h__3_37_);
v_val_41_ = lean_ctor_get(v_val_40_, 0);
lean_inc(v_val_41_);
lean_dec_ref_known(v_val_40_, 1);
v___x_42_ = lean_apply_1(v_h__2_36_, v_val_41_);
return v___x_42_;
}
else
{
lean_object* v_val_43_; lean_object* v___x_44_; 
lean_dec(v_h__2_36_);
v_val_43_ = lean_ctor_get(v_val_40_, 0);
lean_inc(v_val_43_);
lean_dec_ref_known(v_val_40_, 1);
v___x_44_ = lean_apply_1(v_h__3_37_, v_val_43_);
return v___x_44_;
}
}
}
}
LEAN_EXPORT lean_object* lp_formal___private_Formal_InfiniteAggregation_Good_0__InfiniteAggregation_homogeneousCoordinates_match__1_splitter___boxed(lean_object* v_r_45_, lean_object* v_motive_46_, lean_object* v_x_47_, lean_object* v_h__1_48_, lean_object* v_h__2_49_, lean_object* v_h__3_50_){
_start:
{
lean_object* v_res_51_; 
v_res_51_ = lp_formal___private_Formal_InfiniteAggregation_Good_0__InfiniteAggregation_homogeneousCoordinates_match__1_splitter(v_r_45_, v_motive_46_, v_x_47_, v_h__1_48_, v_h__2_49_, v_h__3_50_);
lean_dec(v_r_45_);
return v_res_51_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_formal_Formal_InfiniteAggregation_GoodSpectral(uint8_t builtin);
lean_object* initialize_formal_Formal_InfiniteAggregation_GoodConvex(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_formal_Formal_InfiniteAggregation_Good(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_formal_Formal_InfiniteAggregation_GoodSpectral(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_formal_Formal_InfiniteAggregation_GoodConvex(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
