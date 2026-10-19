import{S as d}from"./index-CT7-cRxi.js";const e="bumpVertexDeclaration",n=`#if defined(BUMP) || defined(PARALLAX) || defined(CLEARCOAT_BUMP) || defined(ANISOTROPIC)
#if defined(TANGENT) && defined(NORMAL) 
varying mat3 vTBN;
#endif
#endif
`;d.IncludesShadersStore[e]||(d.IncludesShadersStore[e]=n);const r={name:e,shader:n};export{r as b};
