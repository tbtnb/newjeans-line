import{S as e}from"./index-CSHHnqPe.js";const t="fogVertexDeclaration",r=`#ifdef FOG
varying vec3 vFogDistance;
#endif
`;e.IncludesShadersStore[t]||(e.IncludesShadersStore[t]=r);const i={name:t,shader:r},o="fogVertex",a=`#ifdef FOG
vFogDistance=(view*worldPos).xyz;
#endif
`;e.IncludesShadersStore[o]||(e.IncludesShadersStore[o]=a);const c={name:o,shader:a},s="logDepthVertex",n=`#ifdef LOGARITHMICDEPTH
vFragmentDepth=1.0+gl_Position.w;gl_Position.z=log2(max(0.000001,vFragmentDepth))*logarithmicDepthConstant;
#endif
`;e.IncludesShadersStore[s]||(e.IncludesShadersStore[s]=n);const f={name:s,shader:n};export{c as a,i as f,f as l};
