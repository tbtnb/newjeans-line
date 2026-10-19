import{S as e}from"./index-DHWCRBEZ.js";import{c as t,a as o}from"./clipPlaneFragment-DkMpXOO8.js";import{l}from"./logDepthDeclaration-DNosAvkK.js";import{l as i}from"./logDepthFragment-Bg57FJVf.js";const r="linePixelShader",a=`#include<clipPlaneFragmentDeclaration>
uniform color: vec4f;
#include<logDepthDeclaration>
#define CUSTOM_FRAGMENT_DEFINITIONS
@fragment
fn main(input: FragmentInputs)->FragmentOutputs {
#define CUSTOM_FRAGMENT_MAIN_BEGIN
#include<logDepthFragment>
#include<clipPlaneFragment>
fragmentOutputs.color=uniforms.color;
#define CUSTOM_FRAGMENT_MAIN_END
}`;e.ShadersStoreWGSL[r]||(e.ShadersStoreWGSL[r]=a);const c=[t,l,i,o];for(const n of c)e.IncludesShadersStoreWGSL[n.name]||(e.IncludesShadersStoreWGSL[n.name]=n.shader);const f={name:r,shader:a};export{f as linePixelShaderWGSL};
