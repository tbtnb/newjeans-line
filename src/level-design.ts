/** Album-derived palettes and original spatial stories. See design/ART_DIRECTION.md. */
export type ArtFamily = 'denim'|'memory'|'pixel'|'mixtape'|'bloom';
export interface LevelArt {
  id:string;
  family:ArtFamily;
  scene:string;
  subtitle:string;
  description:string;
  cover:string;
  concept:string;
  dark:boolean;
  colors:{background:string;ground:string;road:string;roadSide:string;line:string;accent:string;secondary:string;ink:string};
  chapters:string[];
  egg:{at:number;name:string;type:string};
}

const palettes:Record<ArtFamily,LevelArt['colors']> = {
  denim:{background:'#BCD7EE',ground:'#AFCBEB',road:'#F6F4EA',roadSide:'#668DB9',line:'#244EBB',accent:'#244EBB',secondary:'#8FAFD4',ink:'#243F78'},
  memory:{background:'#DEDDE5',ground:'#BECEDC',road:'#F6F0E8',roadSide:'#B28D99',line:'#A92E48',accent:'#A92E48',secondary:'#E4BFC2',ink:'#71334C'},
  pixel:{background:'#AADCF5',ground:'#8CC6DB',road:'#FFF8ED',roadSide:'#7099C6',line:'#DD73B8',accent:'#F18BC8',secondary:'#A3E8C3',ink:'#455D8B'},
  mixtape:{background:'#D8E5D8',ground:'#91AC97',road:'#F5E8BA',roadSide:'#758E99',line:'#D46E56',accent:'#D46E56',secondary:'#769EB4',ink:'#243B51'},
  bloom:{background:'#0D1630',ground:'#253D61',road:'#FFF6D9',roadSide:'#527593',line:'#F36AA7',accent:'#F36AA7',secondary:'#49CDB7',ink:'#11192C'},
};
const covers:Record<ArtFamily,string>={denim:'new-jeans',memory:'omg',pixel:'get-up',mixtape:'how-sweet',bloom:'supernatural'};
type Profile = Pick<LevelArt,'id'|'family'|'scene'|'subtitle'|'description'|'chapters'|'egg'> & {dark?:boolean;colors?:Partial<LevelArt['colors']>};
function profile(p:Profile):LevelArt {
  return {...p,dark:p.dark??false,colors:{...palettes[p.family],...p.colors},cover:`./art/covers/${covers[p.family]}.jpg`,concept:`./art/concepts/${p.family}.png`};
}

export const LEVEL_ART:readonly LevelArt[] = [
  profile({id:'attention',family:'denim',scene:'蓝白操场',subtitle:'午后第一次被看见',description:'从空看台到晴天屋顶，五扇窗慢慢转向同一束光。',chapters:['蓝白操场','窗户街区','屋顶舞场','回到晴天'],egg:{at:.73,name:'五扇回头的窗',type:'turning-windows'}}),
  profile({id:'hype-boy',family:'denim',scene:'屋顶邀请',subtitle:'不同心事，同一场舞会',description:'四封邀请穿过黄昏街区，在唱片镜球下汇成一颗星。',chapters:['黄昏屋顶','四个心事街区','汇合舞会','五盏余灯'],egg:{at:.72,name:'拼成星星的邀请',type:'invitation-star'},colors:{background:'#B6BEDC',ground:'#91A5CC',secondary:'#DDB8CA',accent:'#526DB9'}}),
  profile({id:'cookie',family:'denim',scene:'蓝调音乐工坊',subtitle:'把新音乐烘焙出来',description:'圆片沿工作台变成 CD，小兔把五张新唱片装成礼物。',chapters:['蓝白音乐工坊','圆片输送台','CD 唱片机','礼物封装'],egg:{at:.68,name:'整理五张唱片的小兔',type:'record-bunny'},colors:{secondary:'#B6BDD7',ground:'#A7BED6'}}),
  profile({id:'hurt',family:'denim',scene:'未寄出的温室',subtitle:'留一点勇气给自己',description:'一封未寄出的信、一把空椅子，和天亮前才开放的小花。',chapters:['暖灯窗台','玻璃温室','安静花园','微亮天空'],egg:{at:.83,name:'尾声才开的花',type:'late-flower'},dark:true,colors:{background:'#435D7E',ground:'#607B93',roadSide:'#8DA6B7',line:'#E6C591',accent:'#D9B99A',secondary:'#8CB4BE',ink:'#304B6A'}}),
  profile({id:'omg',family:'memory',scene:'接通的梦',subtitle:'梦里接到你的电话',description:'电话亮屏，消息房间打开，三个小圆点悄悄变成星星。',chapters:['电话亮屏','消息房间','梦境接通','相聚的灯'],egg:{at:.67,name:'纸箱里的猫耳',type:'cat-message'},colors:{background:'#E6D8DE',ground:'#D3B5C2',secondary:'#E8BFC6'}}),
  profile({id:'ditto',family:'memory',scene:'雪中的录像',subtitle:'影像里一直有你',description:'酒红校舍退到雪原，远处的小鹿回头，摄像机的红点仍亮着。',chapters:['旧摄像机','雪中校舍','白色雪原','保存的录像'],egg:{at:.65,name:'雪原上回头的小鹿',type:'deer-camera'},colors:{background:'#D6DFE8',ground:'#C4D1DE',secondary:'#A9C3D4',accent:'#A35669'}}),
  profile({id:'new-jeans',family:'pixel',scene:'活起来的蓝图',subtitle:'新的我，从这里出发',description:'一枚像素点唤醒纸片城市，五色尾迹落在牛仔外套的小徽章上。',chapters:['方格蓝图','纸片城市','五色尾迹','活起来的徽章'],egg:{at:.68,name:'向你点头的小植物',type:'nodding-plant'}}),
  profile({id:'super-shy',family:'pixel',scene:'薄荷色问候',subtitle:'害羞也能带动整座广场',description:'从街角自行车到彩窗巴士，伞后的小兔终于挥了挥手。',chapters:['薄荷街角','公园遮阳伞','阳光广场','彩窗巴士'],egg:{at:.77,name:'伞后挥手的小兔',type:'shy-bunny'},colors:{background:'#C4E8DF',ground:'#94D4BE',accent:'#EF91C0',secondary:'#9AB6E9'}}),
  profile({id:'eta',family:'pixel',scene:'消息正在路上',subtitle:'五扇窗，终于接通',description:'电话与信号塔连接彩窗街区，急切的消息最终抵达长椅旁。',chapters:['电话桌面','传递消息的街区','拼合的现场','两盏长椅灯'],egg:{at:.71,name:'五扇接通的小窗',type:'connected-windows'},colors:{background:'#B9DBEE',ground:'#98BBD8',line:'#D97293',accent:'#E98992',secondary:'#A7D4D3'}}),
  profile({id:'cool-with-you',family:'pixel',scene:'雨中的空画框',subtitle:'被看见的倒影',description:'浅蓝画廊走向开放庭院，一枚羽毛慢慢有了倒影。',chapters:['浅蓝画廊','出现的倒影','雨中庭院','开放出口'],egg:{at:.59,name:'水边羽毛的倒影',type:'feather-reflection'},colors:{background:'#B9CBD6',ground:'#96B0C1',road:'#F3EEDF',roadSide:'#839AAE',line:'#798CB9',accent:'#B7A7C6',secondary:'#D6C6A7',ink:'#52657E'}}),
  profile({id:'get-up',family:'pixel',scene:'雨后，再向前',subtitle:'一口慢慢呼出的气',description:'沿着上一场雨留下的浅水与空画框，走向一点暖光和月绿草地。',chapters:['雨后浅水','一束暖光','地平线','月绿草地'],egg:{at:.61,name:'五粒晨光',type:'dawn-lights'},colors:{background:'#C7DDE3',ground:'#A8C4CD',road:'#FFF6DE',roadSide:'#91ACBE',line:'#B5A5C7',accent:'#D8BC85',secondary:'#AECBB7',ink:'#627C8F'}}),
  profile({id:'asap',family:'pixel',scene:'月光里的约定',subtitle:'明天见，快一点',description:'小钟摆轻声摇动，信封留在花园里，远处小屋终于亮起灯。',chapters:['月绿草地','轻声钟摆','浅水花园','等待亮起的小屋'],egg:{at:.81,name:'相聚的五粒花粉',type:'pollen-clock'},dark:true,colors:{background:'#3B6170',ground:'#638D8C',road:'#F4F0DC',roadSide:'#83A1AD',line:'#D1B2D9',accent:'#E0CEA0',secondary:'#A8CBB0',ink:'#365665'}}),
  profile({id:'how-sweet',family:'mixtape',scene:'唱片店外的晴天',subtitle:'走出自己的好天气',description:'珊瑚磁带门后，遮阳棚逐个打开，旧唱片店翻出一面新的招牌。',chapters:['黑框唱片店','遮阳棚街道','自由舞场','开阔天空'],egg:{at:.75,name:'一口苹果与开门翻牌',type:'apple-sign'}}),
  profile({id:'bubble-gum',family:'mixtape',scene:'海风吹过温室',subtitle:'把夏天轻轻吹起来',description:'海堤、白窗温室与野餐余晖，五颗弹珠守着即将下水的纸船。',chapters:['牛仔蓝海堤','草地温室','海风气球','野餐余晖'],egg:{at:.7,name:'五颗弹珠和纸船',type:'marbles-boat'},colors:{background:'#C5E2E7',ground:'#A0C7CE',roadSide:'#739BB0',line:'#C97B6B',secondary:'#A9C4A2'}}),
  profile({id:'supernatural',family:'bloom',scene:'花形天线的夜晚',subtitle:'心跳接上宇宙的频道',description:'五色刻度渐渐同步，彩虹花形天线转向月亮，屋顶留出观星的位置。',chapters:['深蓝电台屋顶','频道渐同步','彩色花环与月亮','观星位置'],egg:{at:.78,name:'调到同一频道的收音机',type:'radio-tuning'},dark:true}),
  profile({id:'right-now',family:'bloom',scene:'等你回一朵花',subtitle:'回应正在生长',description:'消息入口发芽成温室，五盆花转过身，两只小纸杯递来一朵花。',chapters:['空白消息入口','发芽信箱','花朵温室','稳定暖灯'],egg:{at:.72,name:'纸杯间传递的一朵花',type:'flower-cups'},colors:{background:'#DCE8D7',ground:'#B1CFB8',roadSide:'#849F94',line:'#D6699C',accent:'#E889B4',secondary:'#65BFA3'}}),
];

const byId = new Map(LEVEL_ART.map(art=>[art.id,art]));
/** Unknown old saves remain playable by using the first map's art. */
export function getLevelArt(id:string):LevelArt { return byId.get(id)??LEVEL_ART[0]; }
