(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-7a836d00"],{"0fea":function(e,t,r){"use strict";r.d(t,"c",(function(){return a})),r.d(t,"d",(function(){return c})),r.d(t,"b",(function(){return l})),r.d(t,"a",(function(){return s}));var n=r("b775"),o=(r("bc3a"),"https://qingjiao.shop:8000"),i=o;r("4328"),r("bc3a").default;function a(e){return Object(n["a"])({url:i+"/api/Item/",method:"get",params:{farmname:e}})}function c(e){return Object(n["a"])({url:i+"/api/video/",method:"get",params:{farmname:e}})}function l(e){return Object(n["a"])({url:i+"/api/farm/",method:"GET",params:{farmname:e}})}function s(e){return Object(n["a"])({url:i+"/api/Item/",method:"DELETE",params:{id:e}})}},"25a9":function(e,t,r){"use strict";r.r(t);var n=function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("div",[r("el-container",[r("el-header",[r("li",[e._v("所选商品:"+e._s(e.selectedItem.name))]),e._v(" "),r("image",{attrs:{src:e.picUrl}})]),e._v(" "),r("el-container",[r("el-aside",{attrs:{width:"600px"}},[r("li",[e._v("选择商品")]),e._v(" "),e._l(e.itemsInfo,(function(t){return r("div",[r("el-button",{staticClass:"item_name",on:{click:function(r){return e.choseItem(t)}}},[e._v(e._s(t.name))])],1)}))],2),e._v(" "),r("el-main",[r("li",[e._v("选择视频")]),e._v(" "),r("el-checkbox-group",{on:{change:e.onChange},model:{value:e.selectedVideo,callback:function(t){e.selectedVideo=t},expression:"selectedVideo"}},e._l(e.videosInfo,(function(t){return r("el-checkbox",{key:t.id,staticStyle:{display:"block"},attrs:{label:t.id,border:""}},[e._v(" \n            "+e._s(t.id)+"."+e._s(t.name)+":"+e._s(t.description)+"\n          ")])})),1)],1)],1)],1),e._v(" "),r("el-button",{staticStyle:{top:"200px"},on:{click:function(t){return e.onSubmit()}}},[e._v("\n      绑定视频\n    ")])],1)},o=[],i=r("bc3a"),a=r.n(i),c=r("0fea"),l=r("4360"),s=r("4328"),u=r.n(s),f={name:"VIMap",data:function(){return{itemsInfo:[],videosInfo:[],targetVideos:[],selectedVideo:[],showItem:!0,selectedItem:{},picUrl:""}},created:function(){console.log("---init----",this.$route.params),this.init()},methods:{onSubmit:function(e){var t=[];for(var r in this.selectedVideo)t.push(r);console.log("----ids----",t,this.selectedVideo);var n=u.a.stringify({videoids:this.selectedVideo,itemid:this.selectedItem.id,farmname:l["a"].getters.farmname});console.log("---param---",n),a.a.post("https://qingjiao.shop:8000/api/VIMap/",n).then((function(e){console.log(e),alert("绑定成功")}))},onChange:function(e){console.log(this.selectedVideo)},choseItem:function(e){this.selectedItem=e,console.log(e),this.picUrl="http://qingjiao.shop:8000/static/pic/"+e.pic_address},init:function(){this.VideoList(),this.ItemList()},test:function(e){},select:function(){console.log(this.selectedVideo)},VideoList:function(){var e=this,t=l["a"].getters.farmname;console.log(t),Object(c["d"])(l["a"].getters.farmname).then((function(t){e.videosInfo=t.data,console.log("----videodata----",e.videosInfo)}))},ItemList:function(){var e=this;Object(c["c"])(l["a"].getters.farmname).then((function(t){console.log("itemdata",t.data),e.itemsInfo=t.data}))}}},d=f,p=(r("5c7e"),r("2877")),y=Object(p["a"])(d,n,o,!1,null,"5b56a53e",null);t["default"]=y.exports},"364f":function(e,t,r){},4127:function(e,t,r){"use strict";var n=r("d233"),o=r("b313"),i={brackets:function(e){return e+"[]"},indices:function(e,t){return e+"["+t+"]"},repeat:function(e){return e}},a=Date.prototype.toISOString,c={delimiter:"&",encode:!0,encoder:n.encode,encodeValuesOnly:!1,serializeDate:function(e){return a.call(e)},skipNulls:!1,strictNullHandling:!1},l=function e(t,r,o,i,a,l,s,u,f,d,p,y){var m=t;if("function"===typeof s)m=s(r,m);else if(m instanceof Date)m=d(m);else if(null===m){if(i)return l&&!y?l(r,c.encoder):r;m=""}if("string"===typeof m||"number"===typeof m||"boolean"===typeof m||n.isBuffer(m)){if(l){var h=y?r:l(r,c.encoder);return[p(h)+"="+p(l(m,c.encoder))]}return[p(r)+"="+p(String(m))]}var b,g=[];if("undefined"===typeof m)return g;if(Array.isArray(s))b=s;else{var v=Object.keys(m);b=u?v.sort(u):v}for(var j=0;j<b.length;++j){var O=b[j];a&&null===m[O]||(g=Array.isArray(m)?g.concat(e(m[O],o(r,O),o,i,a,l,s,u,f,d,p,y)):g.concat(e(m[O],r+(f?"."+O:"["+O+"]"),o,i,a,l,s,u,f,d,p,y)))}return g};e.exports=function(e,t){var r=e,a=t?n.assign({},t):{};if(null!==a.encoder&&void 0!==a.encoder&&"function"!==typeof a.encoder)throw new TypeError("Encoder has to be a function.");var s="undefined"===typeof a.delimiter?c.delimiter:a.delimiter,u="boolean"===typeof a.strictNullHandling?a.strictNullHandling:c.strictNullHandling,f="boolean"===typeof a.skipNulls?a.skipNulls:c.skipNulls,d="boolean"===typeof a.encode?a.encode:c.encode,p="function"===typeof a.encoder?a.encoder:c.encoder,y="function"===typeof a.sort?a.sort:null,m="undefined"!==typeof a.allowDots&&a.allowDots,h="function"===typeof a.serializeDate?a.serializeDate:c.serializeDate,b="boolean"===typeof a.encodeValuesOnly?a.encodeValuesOnly:c.encodeValuesOnly;if("undefined"===typeof a.format)a.format=o["default"];else if(!Object.prototype.hasOwnProperty.call(o.formatters,a.format))throw new TypeError("Unknown format option provided.");var g,v,j=o.formatters[a.format];"function"===typeof a.filter?(v=a.filter,r=v("",r)):Array.isArray(a.filter)&&(v=a.filter,g=v);var O,w=[];if("object"!==typeof r||null===r)return"";O=a.arrayFormat in i?a.arrayFormat:"indices"in a?a.indices?"indices":"repeat":"indices";var A=i[O];g||(g=Object.keys(r)),y&&g.sort(y);for(var x=0;x<g.length;++x){var I=g[x];f&&null===r[I]||(w=w.concat(l(r[I],I,A,u,f,d?p:null,v,y,m,h,j,b)))}var _=w.join(s),k=!0===a.addQueryPrefix?"?":"";return _.length>0?k+_:""}},4328:function(e,t,r){"use strict";var n=r("4127"),o=r("9e6a"),i=r("b313");e.exports={formats:i,parse:o,stringify:n}},"5c7e":function(e,t,r){"use strict";var n=r("364f"),o=r.n(n);o.a},"9e6a":function(e,t,r){"use strict";var n=r("d233"),o=Object.prototype.hasOwnProperty,i={allowDots:!1,allowPrototypes:!1,arrayLimit:20,decoder:n.decode,delimiter:"&",depth:5,parameterLimit:1e3,plainObjects:!1,strictNullHandling:!1},a=function(e,t){for(var r={},n=t.ignoreQueryPrefix?e.replace(/^\?/,""):e,a=t.parameterLimit===1/0?void 0:t.parameterLimit,c=n.split(t.delimiter,a),l=0;l<c.length;++l){var s,u,f=c[l],d=f.indexOf("]="),p=-1===d?f.indexOf("="):d+1;-1===p?(s=t.decoder(f,i.decoder),u=t.strictNullHandling?null:""):(s=t.decoder(f.slice(0,p),i.decoder),u=t.decoder(f.slice(p+1),i.decoder)),o.call(r,s)?r[s]=[].concat(r[s]).concat(u):r[s]=u}return r},c=function(e,t,r){for(var n=t,o=e.length-1;o>=0;--o){var i,a=e[o];if("[]"===a)i=[],i=i.concat(n);else{i=r.plainObjects?Object.create(null):{};var c="["===a.charAt(0)&&"]"===a.charAt(a.length-1)?a.slice(1,-1):a,l=parseInt(c,10);!isNaN(l)&&a!==c&&String(l)===c&&l>=0&&r.parseArrays&&l<=r.arrayLimit?(i=[],i[l]=n):i[c]=n}n=i}return n},l=function(e,t,r){if(e){var n=r.allowDots?e.replace(/\.([^.[]+)/g,"[$1]"):e,i=/(\[[^[\]]*])/,a=/(\[[^[\]]*])/g,l=i.exec(n),s=l?n.slice(0,l.index):n,u=[];if(s){if(!r.plainObjects&&o.call(Object.prototype,s)&&!r.allowPrototypes)return;u.push(s)}var f=0;while(null!==(l=a.exec(n))&&f<r.depth){if(f+=1,!r.plainObjects&&o.call(Object.prototype,l[1].slice(1,-1))&&!r.allowPrototypes)return;u.push(l[1])}return l&&u.push("["+n.slice(l.index)+"]"),c(u,t,r)}};e.exports=function(e,t){var r=t?n.assign({},t):{};if(null!==r.decoder&&void 0!==r.decoder&&"function"!==typeof r.decoder)throw new TypeError("Decoder has to be a function.");if(r.ignoreQueryPrefix=!0===r.ignoreQueryPrefix,r.delimiter="string"===typeof r.delimiter||n.isRegExp(r.delimiter)?r.delimiter:i.delimiter,r.depth="number"===typeof r.depth?r.depth:i.depth,r.arrayLimit="number"===typeof r.arrayLimit?r.arrayLimit:i.arrayLimit,r.parseArrays=!1!==r.parseArrays,r.decoder="function"===typeof r.decoder?r.decoder:i.decoder,r.allowDots="boolean"===typeof r.allowDots?r.allowDots:i.allowDots,r.plainObjects="boolean"===typeof r.plainObjects?r.plainObjects:i.plainObjects,r.allowPrototypes="boolean"===typeof r.allowPrototypes?r.allowPrototypes:i.allowPrototypes,r.parameterLimit="number"===typeof r.parameterLimit?r.parameterLimit:i.parameterLimit,r.strictNullHandling="boolean"===typeof r.strictNullHandling?r.strictNullHandling:i.strictNullHandling,""===e||null===e||"undefined"===typeof e)return r.plainObjects?Object.create(null):{};for(var o="string"===typeof e?a(e,r):e,c=r.plainObjects?Object.create(null):{},s=Object.keys(o),u=0;u<s.length;++u){var f=s[u],d=l(f,o[f],r);c=n.merge(c,d,r)}return n.compact(c)}},b313:function(e,t,r){"use strict";var n=String.prototype.replace,o=/%20/g;e.exports={default:"RFC3986",formatters:{RFC1738:function(e){return n.call(e,o,"+")},RFC3986:function(e){return e}},RFC1738:"RFC1738",RFC3986:"RFC3986"}},d233:function(e,t,r){"use strict";var n=Object.prototype.hasOwnProperty,o=function(){for(var e=[],t=0;t<256;++t)e.push("%"+((t<16?"0":"")+t.toString(16)).toUpperCase());return e}(),i=function(e){var t;while(e.length){var r=e.pop();if(t=r.obj[r.prop],Array.isArray(t)){for(var n=[],o=0;o<t.length;++o)"undefined"!==typeof t[o]&&n.push(t[o]);r.obj[r.prop]=n}}return t},a=function(e,t){for(var r=t&&t.plainObjects?Object.create(null):{},n=0;n<e.length;++n)"undefined"!==typeof e[n]&&(r[n]=e[n]);return r},c=function e(t,r,o){if(!r)return t;if("object"!==typeof r){if(Array.isArray(t))t.push(r);else{if("object"!==typeof t)return[t,r];(o.plainObjects||o.allowPrototypes||!n.call(Object.prototype,r))&&(t[r]=!0)}return t}if("object"!==typeof t)return[t].concat(r);var i=t;return Array.isArray(t)&&!Array.isArray(r)&&(i=a(t,o)),Array.isArray(t)&&Array.isArray(r)?(r.forEach((function(r,i){n.call(t,i)?t[i]&&"object"===typeof t[i]?t[i]=e(t[i],r,o):t.push(r):t[i]=r})),t):Object.keys(r).reduce((function(t,i){var a=r[i];return n.call(t,i)?t[i]=e(t[i],a,o):t[i]=a,t}),i)},l=function(e,t){return Object.keys(t).reduce((function(e,r){return e[r]=t[r],e}),e)},s=function(e){try{return decodeURIComponent(e.replace(/\+/g," "))}catch(t){return e}},u=function(e){if(0===e.length)return e;for(var t="string"===typeof e?e:String(e),r="",n=0;n<t.length;++n){var i=t.charCodeAt(n);45===i||46===i||95===i||126===i||i>=48&&i<=57||i>=65&&i<=90||i>=97&&i<=122?r+=t.charAt(n):i<128?r+=o[i]:i<2048?r+=o[192|i>>6]+o[128|63&i]:i<55296||i>=57344?r+=o[224|i>>12]+o[128|i>>6&63]+o[128|63&i]:(n+=1,i=65536+((1023&i)<<10|1023&t.charCodeAt(n)),r+=o[240|i>>18]+o[128|i>>12&63]+o[128|i>>6&63]+o[128|63&i])}return r},f=function(e){for(var t=[{obj:{o:e},prop:"o"}],r=[],n=0;n<t.length;++n)for(var o=t[n],a=o.obj[o.prop],c=Object.keys(a),l=0;l<c.length;++l){var s=c[l],u=a[s];"object"===typeof u&&null!==u&&-1===r.indexOf(u)&&(t.push({obj:a,prop:s}),r.push(u))}return i(t)},d=function(e){return"[object RegExp]"===Object.prototype.toString.call(e)},p=function(e){return null!==e&&"undefined"!==typeof e&&!!(e.constructor&&e.constructor.isBuffer&&e.constructor.isBuffer(e))};e.exports={arrayToObject:a,assign:l,compact:f,decode:s,encode:u,isBuffer:p,isRegExp:d,merge:c}}}]);