// Lean compiler output
// Module: Formal.InfiniteAggregation.GoodMatrix
// Imports: public import Init public meta import Init public import Formal.QuadraticPrecision.Spectral
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
extern lean_object* lp_mathlib_Real_definition_00___x40_Mathlib_Data_Real_Basic_1850581184____hygCtx___hyg_8_;
lean_object* lp_mathlib_Real_definition___lam__0_00___x40_Mathlib_Data_Real_Basic_4214226450____hygCtx___hyg_8_(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal___private_Formal_InfiniteAggregation_GoodMatrix_0__InfiniteAggregation_homogeneousMatrix_match__1_splitter___redArg(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal___private_Formal_InfiniteAggregation_GoodMatrix_0__InfiniteAggregation_homogeneousMatrix_match__1_splitter(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal___private_Formal_InfiniteAggregation_GoodMatrix_0__InfiniteAggregation_homogeneousMatrix_match__1_splitter___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal___private_Formal_InfiniteAggregation_GoodMatrix_0__InfiniteAggregation_replicateDirection_match__1_splitter___redArg(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal___private_Formal_InfiniteAggregation_GoodMatrix_0__InfiniteAggregation_replicateDirection_match__1_splitter(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal___private_Formal_InfiniteAggregation_GoodMatrix_0__InfiniteAggregation_replicateDirection_match__1_splitter___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_replicateDirection___redArg___lam__0(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_replicateDirection___redArg(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_replicateDirection(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_replicateDirection___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_formal___private_Formal_InfiniteAggregation_GoodMatrix_0__InfiniteAggregation_homogeneousMatrix_match__1_splitter___redArg(lean_object* v_x_1_, lean_object* v_x_2_, lean_object* v_h__1_3_, lean_object* v_h__2_4_, lean_object* v_h__3_5_, lean_object* v_h__4_6_, lean_object* v_h__5_7_, lean_object* v_h__6_8_){
_start:
{
if (lean_obj_tag(v_x_1_) == 0)
{
lean_dec(v_h__5_7_);
lean_dec(v_h__4_6_);
lean_dec(v_h__3_5_);
lean_dec(v_h__2_4_);
if (lean_obj_tag(v_x_2_) == 0)
{
lean_object* v___x_9_; lean_object* v___x_10_; 
lean_dec(v_h__6_8_);
v___x_9_ = lean_box(0);
v___x_10_ = lean_apply_1(v_h__1_3_, v___x_9_);
return v___x_10_;
}
else
{
lean_object* v___x_11_; 
lean_dec(v_h__1_3_);
v___x_11_ = lean_apply_7(v_h__6_8_, v_x_1_, v_x_2_, lean_box(0), lean_box(0), lean_box(0), lean_box(0), lean_box(0));
return v___x_11_;
}
}
else
{
lean_object* v_val_12_; 
lean_dec(v_h__1_3_);
v_val_12_ = lean_ctor_get(v_x_1_, 0);
if (lean_obj_tag(v_val_12_) == 0)
{
lean_dec(v_h__5_7_);
lean_dec(v_h__3_5_);
if (lean_obj_tag(v_x_2_) == 1)
{
lean_object* v_val_13_; 
lean_inc_ref(v_val_12_);
lean_dec_ref_known(v_x_1_, 1);
lean_dec(v_h__6_8_);
v_val_13_ = lean_ctor_get(v_x_2_, 0);
lean_inc(v_val_13_);
lean_dec_ref_known(v_x_2_, 1);
if (lean_obj_tag(v_val_13_) == 0)
{
lean_object* v_val_14_; lean_object* v_val_15_; lean_object* v___x_16_; 
lean_dec(v_h__4_6_);
v_val_14_ = lean_ctor_get(v_val_12_, 0);
lean_inc(v_val_14_);
lean_dec_ref_known(v_val_12_, 1);
v_val_15_ = lean_ctor_get(v_val_13_, 0);
lean_inc(v_val_15_);
lean_dec_ref_known(v_val_13_, 1);
v___x_16_ = lean_apply_2(v_h__2_4_, v_val_14_, v_val_15_);
return v___x_16_;
}
else
{
lean_object* v_val_17_; lean_object* v_val_18_; lean_object* v___x_19_; 
lean_dec(v_h__2_4_);
v_val_17_ = lean_ctor_get(v_val_12_, 0);
lean_inc(v_val_17_);
lean_dec_ref_known(v_val_12_, 1);
v_val_18_ = lean_ctor_get(v_val_13_, 0);
lean_inc(v_val_18_);
lean_dec_ref_known(v_val_13_, 1);
v___x_19_ = lean_apply_2(v_h__4_6_, v_val_17_, v_val_18_);
return v___x_19_;
}
}
else
{
lean_object* v___x_20_; 
lean_dec(v_h__4_6_);
lean_dec(v_h__2_4_);
v___x_20_ = lean_apply_7(v_h__6_8_, v_x_1_, v_x_2_, lean_box(0), lean_box(0), lean_box(0), lean_box(0), lean_box(0));
return v___x_20_;
}
}
else
{
lean_dec(v_h__4_6_);
lean_dec(v_h__2_4_);
if (lean_obj_tag(v_x_2_) == 1)
{
lean_object* v_val_21_; 
lean_inc_ref(v_val_12_);
lean_dec_ref_known(v_x_1_, 1);
lean_dec(v_h__6_8_);
v_val_21_ = lean_ctor_get(v_x_2_, 0);
lean_inc(v_val_21_);
lean_dec_ref_known(v_x_2_, 1);
if (lean_obj_tag(v_val_21_) == 0)
{
lean_object* v_val_22_; lean_object* v_val_23_; lean_object* v___x_24_; 
lean_dec(v_h__3_5_);
v_val_22_ = lean_ctor_get(v_val_12_, 0);
lean_inc(v_val_22_);
lean_dec_ref_known(v_val_12_, 1);
v_val_23_ = lean_ctor_get(v_val_21_, 0);
lean_inc(v_val_23_);
lean_dec_ref_known(v_val_21_, 1);
v___x_24_ = lean_apply_2(v_h__5_7_, v_val_22_, v_val_23_);
return v___x_24_;
}
else
{
lean_object* v_val_25_; lean_object* v_val_26_; lean_object* v___x_27_; 
lean_dec(v_h__5_7_);
v_val_25_ = lean_ctor_get(v_val_12_, 0);
lean_inc(v_val_25_);
lean_dec_ref_known(v_val_12_, 1);
v_val_26_ = lean_ctor_get(v_val_21_, 0);
lean_inc(v_val_26_);
lean_dec_ref_known(v_val_21_, 1);
v___x_27_ = lean_apply_2(v_h__3_5_, v_val_25_, v_val_26_);
return v___x_27_;
}
}
else
{
lean_object* v___x_28_; 
lean_dec(v_h__5_7_);
lean_dec(v_h__3_5_);
v___x_28_ = lean_apply_7(v_h__6_8_, v_x_1_, v_x_2_, lean_box(0), lean_box(0), lean_box(0), lean_box(0), lean_box(0));
return v___x_28_;
}
}
}
}
}
LEAN_EXPORT lean_object* lp_formal___private_Formal_InfiniteAggregation_GoodMatrix_0__InfiniteAggregation_homogeneousMatrix_match__1_splitter(lean_object* v_r_29_, lean_object* v_motive_30_, lean_object* v_x_31_, lean_object* v_x_32_, lean_object* v_h__1_33_, lean_object* v_h__2_34_, lean_object* v_h__3_35_, lean_object* v_h__4_36_, lean_object* v_h__5_37_, lean_object* v_h__6_38_){
_start:
{
if (lean_obj_tag(v_x_31_) == 0)
{
lean_dec(v_h__5_37_);
lean_dec(v_h__4_36_);
lean_dec(v_h__3_35_);
lean_dec(v_h__2_34_);
if (lean_obj_tag(v_x_32_) == 0)
{
lean_object* v___x_39_; lean_object* v___x_40_; 
lean_dec(v_h__6_38_);
v___x_39_ = lean_box(0);
v___x_40_ = lean_apply_1(v_h__1_33_, v___x_39_);
return v___x_40_;
}
else
{
lean_object* v___x_41_; 
lean_dec(v_h__1_33_);
v___x_41_ = lean_apply_7(v_h__6_38_, v_x_31_, v_x_32_, lean_box(0), lean_box(0), lean_box(0), lean_box(0), lean_box(0));
return v___x_41_;
}
}
else
{
lean_object* v_val_42_; 
lean_dec(v_h__1_33_);
v_val_42_ = lean_ctor_get(v_x_31_, 0);
if (lean_obj_tag(v_val_42_) == 0)
{
lean_dec(v_h__5_37_);
lean_dec(v_h__3_35_);
if (lean_obj_tag(v_x_32_) == 1)
{
lean_object* v_val_43_; 
lean_inc_ref(v_val_42_);
lean_dec_ref_known(v_x_31_, 1);
lean_dec(v_h__6_38_);
v_val_43_ = lean_ctor_get(v_x_32_, 0);
lean_inc(v_val_43_);
lean_dec_ref_known(v_x_32_, 1);
if (lean_obj_tag(v_val_43_) == 0)
{
lean_object* v_val_44_; lean_object* v_val_45_; lean_object* v___x_46_; 
lean_dec(v_h__4_36_);
v_val_44_ = lean_ctor_get(v_val_42_, 0);
lean_inc(v_val_44_);
lean_dec_ref_known(v_val_42_, 1);
v_val_45_ = lean_ctor_get(v_val_43_, 0);
lean_inc(v_val_45_);
lean_dec_ref_known(v_val_43_, 1);
v___x_46_ = lean_apply_2(v_h__2_34_, v_val_44_, v_val_45_);
return v___x_46_;
}
else
{
lean_object* v_val_47_; lean_object* v_val_48_; lean_object* v___x_49_; 
lean_dec(v_h__2_34_);
v_val_47_ = lean_ctor_get(v_val_42_, 0);
lean_inc(v_val_47_);
lean_dec_ref_known(v_val_42_, 1);
v_val_48_ = lean_ctor_get(v_val_43_, 0);
lean_inc(v_val_48_);
lean_dec_ref_known(v_val_43_, 1);
v___x_49_ = lean_apply_2(v_h__4_36_, v_val_47_, v_val_48_);
return v___x_49_;
}
}
else
{
lean_object* v___x_50_; 
lean_dec(v_h__4_36_);
lean_dec(v_h__2_34_);
v___x_50_ = lean_apply_7(v_h__6_38_, v_x_31_, v_x_32_, lean_box(0), lean_box(0), lean_box(0), lean_box(0), lean_box(0));
return v___x_50_;
}
}
else
{
lean_dec(v_h__4_36_);
lean_dec(v_h__2_34_);
if (lean_obj_tag(v_x_32_) == 1)
{
lean_object* v_val_51_; 
lean_inc_ref(v_val_42_);
lean_dec_ref_known(v_x_31_, 1);
lean_dec(v_h__6_38_);
v_val_51_ = lean_ctor_get(v_x_32_, 0);
lean_inc(v_val_51_);
lean_dec_ref_known(v_x_32_, 1);
if (lean_obj_tag(v_val_51_) == 0)
{
lean_object* v_val_52_; lean_object* v_val_53_; lean_object* v___x_54_; 
lean_dec(v_h__3_35_);
v_val_52_ = lean_ctor_get(v_val_42_, 0);
lean_inc(v_val_52_);
lean_dec_ref_known(v_val_42_, 1);
v_val_53_ = lean_ctor_get(v_val_51_, 0);
lean_inc(v_val_53_);
lean_dec_ref_known(v_val_51_, 1);
v___x_54_ = lean_apply_2(v_h__5_37_, v_val_52_, v_val_53_);
return v___x_54_;
}
else
{
lean_object* v_val_55_; lean_object* v_val_56_; lean_object* v___x_57_; 
lean_dec(v_h__5_37_);
v_val_55_ = lean_ctor_get(v_val_42_, 0);
lean_inc(v_val_55_);
lean_dec_ref_known(v_val_42_, 1);
v_val_56_ = lean_ctor_get(v_val_51_, 0);
lean_inc(v_val_56_);
lean_dec_ref_known(v_val_51_, 1);
v___x_57_ = lean_apply_2(v_h__3_35_, v_val_55_, v_val_56_);
return v___x_57_;
}
}
else
{
lean_object* v___x_58_; 
lean_dec(v_h__5_37_);
lean_dec(v_h__3_35_);
v___x_58_ = lean_apply_7(v_h__6_38_, v_x_31_, v_x_32_, lean_box(0), lean_box(0), lean_box(0), lean_box(0), lean_box(0));
return v___x_58_;
}
}
}
}
}
LEAN_EXPORT lean_object* lp_formal___private_Formal_InfiniteAggregation_GoodMatrix_0__InfiniteAggregation_homogeneousMatrix_match__1_splitter___boxed(lean_object* v_r_59_, lean_object* v_motive_60_, lean_object* v_x_61_, lean_object* v_x_62_, lean_object* v_h__1_63_, lean_object* v_h__2_64_, lean_object* v_h__3_65_, lean_object* v_h__4_66_, lean_object* v_h__5_67_, lean_object* v_h__6_68_){
_start:
{
lean_object* v_res_69_; 
v_res_69_ = lp_formal___private_Formal_InfiniteAggregation_GoodMatrix_0__InfiniteAggregation_homogeneousMatrix_match__1_splitter(v_r_59_, v_motive_60_, v_x_61_, v_x_62_, v_h__1_63_, v_h__2_64_, v_h__3_65_, v_h__4_66_, v_h__5_67_, v_h__6_68_);
lean_dec(v_r_59_);
return v_res_69_;
}
}
LEAN_EXPORT lean_object* lp_formal___private_Formal_InfiniteAggregation_GoodMatrix_0__InfiniteAggregation_replicateDirection_match__1_splitter___redArg(lean_object* v_i_70_, lean_object* v_h__1_71_, lean_object* v_h__2_72_, lean_object* v_h__3_73_){
_start:
{
if (lean_obj_tag(v_i_70_) == 0)
{
lean_object* v___x_74_; lean_object* v___x_75_; 
lean_dec(v_h__3_73_);
lean_dec(v_h__2_72_);
v___x_74_ = lean_box(0);
v___x_75_ = lean_apply_1(v_h__1_71_, v___x_74_);
return v___x_75_;
}
else
{
lean_object* v_val_76_; 
lean_dec(v_h__1_71_);
v_val_76_ = lean_ctor_get(v_i_70_, 0);
lean_inc(v_val_76_);
lean_dec_ref_known(v_i_70_, 1);
if (lean_obj_tag(v_val_76_) == 0)
{
lean_object* v_val_77_; lean_object* v___x_78_; 
lean_dec(v_h__3_73_);
v_val_77_ = lean_ctor_get(v_val_76_, 0);
lean_inc(v_val_77_);
lean_dec_ref_known(v_val_76_, 1);
v___x_78_ = lean_apply_1(v_h__2_72_, v_val_77_);
return v___x_78_;
}
else
{
lean_object* v_val_79_; lean_object* v___x_80_; 
lean_dec(v_h__2_72_);
v_val_79_ = lean_ctor_get(v_val_76_, 0);
lean_inc(v_val_79_);
lean_dec_ref_known(v_val_76_, 1);
v___x_80_ = lean_apply_1(v_h__3_73_, v_val_79_);
return v___x_80_;
}
}
}
}
LEAN_EXPORT lean_object* lp_formal___private_Formal_InfiniteAggregation_GoodMatrix_0__InfiniteAggregation_replicateDirection_match__1_splitter(lean_object* v_r_81_, lean_object* v_motive_82_, lean_object* v_i_83_, lean_object* v_h__1_84_, lean_object* v_h__2_85_, lean_object* v_h__3_86_){
_start:
{
if (lean_obj_tag(v_i_83_) == 0)
{
lean_object* v___x_87_; lean_object* v___x_88_; 
lean_dec(v_h__3_86_);
lean_dec(v_h__2_85_);
v___x_87_ = lean_box(0);
v___x_88_ = lean_apply_1(v_h__1_84_, v___x_87_);
return v___x_88_;
}
else
{
lean_object* v_val_89_; 
lean_dec(v_h__1_84_);
v_val_89_ = lean_ctor_get(v_i_83_, 0);
lean_inc(v_val_89_);
lean_dec_ref_known(v_i_83_, 1);
if (lean_obj_tag(v_val_89_) == 0)
{
lean_object* v_val_90_; lean_object* v___x_91_; 
lean_dec(v_h__3_86_);
v_val_90_ = lean_ctor_get(v_val_89_, 0);
lean_inc(v_val_90_);
lean_dec_ref_known(v_val_89_, 1);
v___x_91_ = lean_apply_1(v_h__2_85_, v_val_90_);
return v___x_91_;
}
else
{
lean_object* v_val_92_; lean_object* v___x_93_; 
lean_dec(v_h__2_85_);
v_val_92_ = lean_ctor_get(v_val_89_, 0);
lean_inc(v_val_92_);
lean_dec_ref_known(v_val_89_, 1);
v___x_93_ = lean_apply_1(v_h__3_86_, v_val_92_);
return v___x_93_;
}
}
}
}
LEAN_EXPORT lean_object* lp_formal___private_Formal_InfiniteAggregation_GoodMatrix_0__InfiniteAggregation_replicateDirection_match__1_splitter___boxed(lean_object* v_r_94_, lean_object* v_motive_95_, lean_object* v_i_96_, lean_object* v_h__1_97_, lean_object* v_h__2_98_, lean_object* v_h__3_99_){
_start:
{
lean_object* v_res_100_; 
v_res_100_ = lp_formal___private_Formal_InfiniteAggregation_GoodMatrix_0__InfiniteAggregation_replicateDirection_match__1_splitter(v_r_94_, v_motive_95_, v_i_96_, v_h__1_97_, v_h__2_98_, v_h__3_99_);
lean_dec(v_r_94_);
return v_res_100_;
}
}
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_replicateDirection___redArg___lam__0(lean_object* v_a_101_, lean_object* v_b_102_, lean_object* v_y_103_, lean_object* v_i_104_){
_start:
{
if (lean_obj_tag(v_i_104_) == 0)
{
lean_object* v___x_105_; 
lean_dec(v_y_103_);
lean_dec(v_b_102_);
lean_dec(v_a_101_);
v___x_105_ = lp_mathlib_Real_definition_00___x40_Mathlib_Data_Real_Basic_1850581184____hygCtx___hyg_8_;
return v___x_105_;
}
else
{
lean_object* v_val_106_; 
v_val_106_ = lean_ctor_get(v_i_104_, 0);
lean_inc(v_val_106_);
lean_dec_ref_known(v_i_104_, 1);
if (lean_obj_tag(v_val_106_) == 0)
{
lean_object* v_val_107_; lean_object* v___x_108_; lean_object* v___f_109_; 
lean_dec(v_b_102_);
v_val_107_ = lean_ctor_get(v_val_106_, 0);
lean_inc(v_val_107_);
lean_dec_ref_known(v_val_106_, 1);
v___x_108_ = lean_apply_1(v_y_103_, v_val_107_);
v___f_109_ = lean_alloc_closure((void*)(lp_mathlib_Real_definition___lam__0_00___x40_Mathlib_Data_Real_Basic_4214226450____hygCtx___hyg_8_), 3, 2);
lean_closure_set(v___f_109_, 0, v_a_101_);
lean_closure_set(v___f_109_, 1, v___x_108_);
return v___f_109_;
}
else
{
lean_object* v_val_110_; lean_object* v___x_111_; lean_object* v___f_112_; 
lean_dec(v_a_101_);
v_val_110_ = lean_ctor_get(v_val_106_, 0);
lean_inc(v_val_110_);
lean_dec_ref_known(v_val_106_, 1);
v___x_111_ = lean_apply_1(v_y_103_, v_val_110_);
v___f_112_ = lean_alloc_closure((void*)(lp_mathlib_Real_definition___lam__0_00___x40_Mathlib_Data_Real_Basic_4214226450____hygCtx___hyg_8_), 3, 2);
lean_closure_set(v___f_112_, 0, v_b_102_);
lean_closure_set(v___f_112_, 1, v___x_111_);
return v___f_112_;
}
}
}
}
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_replicateDirection___redArg(lean_object* v_a_113_, lean_object* v_b_114_){
_start:
{
lean_object* v___f_115_; 
v___f_115_ = lean_alloc_closure((void*)(lp_formal_InfiniteAggregation_replicateDirection___redArg___lam__0), 4, 2);
lean_closure_set(v___f_115_, 0, v_a_113_);
lean_closure_set(v___f_115_, 1, v_b_114_);
return v___f_115_;
}
}
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_replicateDirection(lean_object* v_r_116_, lean_object* v_a_117_, lean_object* v_b_118_){
_start:
{
lean_object* v___f_119_; 
v___f_119_ = lean_alloc_closure((void*)(lp_formal_InfiniteAggregation_replicateDirection___redArg___lam__0), 4, 2);
lean_closure_set(v___f_119_, 0, v_a_117_);
lean_closure_set(v___f_119_, 1, v_b_118_);
return v___f_119_;
}
}
LEAN_EXPORT lean_object* lp_formal_InfiniteAggregation_replicateDirection___boxed(lean_object* v_r_120_, lean_object* v_a_121_, lean_object* v_b_122_){
_start:
{
lean_object* v_res_123_; 
v_res_123_ = lp_formal_InfiniteAggregation_replicateDirection(v_r_120_, v_a_121_, v_b_122_);
lean_dec(v_r_120_);
return v_res_123_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_formal_Formal_QuadraticPrecision_Spectral(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_formal_Formal_InfiniteAggregation_GoodMatrix(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_formal_Formal_QuadraticPrecision_Spectral(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
