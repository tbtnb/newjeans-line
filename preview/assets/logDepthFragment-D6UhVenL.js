import{S as e}from"./index-CjZIo4Fj.js";const t="logDepthFragment",r=`#ifdef LOGARITHMICDEPTH
fragmentOutputs.fragDepth=log2(fragmentInputs.vFragmentDepth)*uniforms.logarithmicDepthConstant*0.5;
#endif
`;e.IncludesShadersStoreWGSL[t]||(e.IncludesShadersStoreWGSL[t]=r);const a={name:t,shader:r};export{a as l};
