import{S as e}from"./index-Cxi1ycvQ.js";import{c as o,a as i}from"./clipPlaneFragment-69ZyY176.js";import{l}from"./logDepthDeclaration-BRGXQvuR.js";import{l as t}from"./logDepthFragment-th9ZTVkQ.js";const a="linePixelShader",r=`#include<clipPlaneFragmentDeclaration>
uniform vec4 color;
#ifdef LOGARITHMICDEPTH
#extension GL_EXT_frag_depth : enable
#endif
#include<logDepthDeclaration>
#define CUSTOM_FRAGMENT_DEFINITIONS
void main(void) {
#define CUSTOM_FRAGMENT_MAIN_BEGIN
#include<logDepthFragment>
#include<clipPlaneFragment>
gl_FragColor=color;
#define CUSTOM_FRAGMENT_MAIN_END
}`;e.ShadersStore[a]||(e.ShadersStore[a]=r);const c=[o,l,t,i];for(const n of c)e.IncludesShadersStore[n.name]||(e.IncludesShadersStore[n.name]=n.shader);const f={name:a,shader:r};export{f as linePixelShader};
