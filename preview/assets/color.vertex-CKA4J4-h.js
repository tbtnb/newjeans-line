import{S as e}from"./index-D4V8c9tG.js";import{b as r,a as t,c as a,d}from"./bakedVertexAnimation-Zk5twH2k.js";import{c,a as l}from"./clipPlaneVertex-BcwdAUrd.js";import{f as s,a as f}from"./fogVertex-DAwg5XHr.js";import{i as m}from"./instancesDeclaration-MVAZ2b6w.js";import{i as V}from"./instancesVertex-BjbJ6ziL.js";import{v as x}from"./vertexColorMixing-Bxu4oOTE.js";const o="colorVertexShader",n=`attribute vec3 position;
#ifdef VERTEXCOLOR
attribute vec4 color;
#endif
#include<bonesDeclaration>
#include<bakedVertexAnimationDeclaration>
#include<clipPlaneVertexDeclaration>
#include<fogVertexDeclaration>
#ifdef FOG
uniform mat4 view;
#endif
#include<instancesDeclaration>
uniform mat4 viewProjection;
#ifdef MULTIVIEW
uniform mat4 viewProjectionR;
#endif
#if defined(VERTEXCOLOR) || defined(INSTANCESCOLOR) && defined(INSTANCES)
varying vec4 vColor;
#endif
#define CUSTOM_VERTEX_DEFINITIONS
void main(void) {
#define CUSTOM_VERTEX_MAIN_BEGIN
#ifdef VERTEXCOLOR
vec4 colorUpdated=color;
#endif
#include<instancesVertex>
#include<bonesVertex>
#include<bakedVertexAnimation>
vec4 worldPos=finalWorld*vec4(position,1.0);
#ifdef MULTIVIEW
if (gl_ViewID_OVR==0u) {gl_Position=viewProjection*worldPos;} else {gl_Position=viewProjectionR*worldPos;}
#else
gl_Position=viewProjection*worldPos;
#endif
#include<clipPlaneVertex>
#include<fogVertex>
#include<vertexColorMixing>
#define CUSTOM_VERTEX_MAIN_END
}`;e.ShadersStore[o]||(e.ShadersStore[o]=n);const S=[r,t,c,s,m,V,a,d,l,f,x];for(const i of S)e.IncludesShadersStore[i.name]||(e.IncludesShadersStore[i.name]=i.shader);const T={name:o,shader:n};export{T as colorVertexShader};
