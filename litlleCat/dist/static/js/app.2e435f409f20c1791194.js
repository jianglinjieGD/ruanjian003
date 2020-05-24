webpackJsonp([1],{"1/2E":function(t,e){},"2/Xu":function(t,e){},"21cN":function(t,e){},"4byl":function(t,e){},"5Gq2":function(t,e){},"6GzY":function(t,e){},"9n10":function(t,e){},IIuS:function(t,e){},KXX2:function(t,e){},LeWD:function(t,e){},M6Sr:function(t,e){},NHnr:function(t,e,s){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var i=s("7+uW"),a={render:function(){var t=this.$createElement,e=this._self._c||t;return e("div",{attrs:{id:"app"}},[e("router-view")],1)},staticRenderFns:[]};var n=s("VU/8")({name:"App"},a,!1,function(t){s("cqTP")},null,null).exports,o=s("I29D"),r=s.n(o),c=s("/ocq"),l={name:"Avatar",props:{imgUrl:String}},u={render:function(){var t=this.$createElement,e=this._self._c||t;return e("div",{staticClass:"user-avatar"},[e("img",{staticClass:"user-img",attrs:{src:this.imgUrl}})])},staticRenderFns:[]};var d=s("VU/8")(l,u,!1,function(t){s("XcuN")},"data-v-03bee622",null).exports,m={name:"HomeHeader",data:function(){return{input:"",list:[{id:1,content:"godd"}]}},components:{Avatar:d},mounted:function(){},methods:{getDetailInfo:function(){r.a.get("/api/allClass",{params:{search:this.input}}).then(this.getDataSucc)},getDataSucc:function(t){t=t.data,this.list=t.data.movieList},itemClick:function(t){this.$router.push("/detail/"+t.target.dataset.id)}},watch:{input:function(){this.getDetailInfo()}}},v={render:function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",{staticClass:"header-wrapper"},[s("div",{staticClass:"header"},[s("div",{staticClass:"header-left",on:{click:function(e){return t.$emit("sidebar")}}},[s("div",{staticClass:"iconfont side-icon"},[t._v("")])]),t._v(" "),s("div",{staticClass:"header-input"},[s("input",{directives:[{name:"model",rawName:"v-model",value:t.input,expression:"input"}],staticClass:"input",attrs:{type:"text",placeholder:"请输入查询电影信息"},domProps:{value:t.input},on:{input:function(e){e.target.composing||(t.input=e.target.value)}}}),t._v(" "),s("div",{staticClass:"iconfont search-icon"},[t._v("")])]),t._v(" "),this.$store.state.userStatus?s("avatar",{staticClass:"avatar",attrs:{imgUrl:"static/avatar.jpeg"}}):s("div",{staticClass:"header-user",on:{click:function(e){return t.$emit("userbox")}}},[s("div",{staticClass:"iconfont user-icon"},[t._v("\n        \n      ")])])],1),t._v(" "),s("div",{directives:[{name:"show",rawName:"v-show",value:t.input,expression:"input"}],ref:"search",staticClass:"search-content"},[s("div",[t._l(t.list,function(e){return s("div",{key:e.movie_id,tag:"div",staticClass:"search-item border-bottom",attrs:{"data-id":e.movie_id},on:{click:function(e){return e.preventDefault(),t.itemClick(e)}}},[t._v("\n        "+t._s(e.name)+"\n      ")])}),t._v(" "),t.list.length?t._e():s("div",{staticClass:"search-item border-bottom"},[t._v("未找到匹配电影")])],2)])])},staticRenderFns:[]};var h=s("VU/8")(m,v,!1,function(t){s("wlhz")},"data-v-64a226e9",null).exports,p={name:"HomeSwiper",props:{list:Array},data:function(){return{swiperOption:{pagination:{el:".swiper-pagination"},loop:!0}}},computed:{showSwiper:function(){return this.list.length}}},f={render:function(){var t=this.$createElement,e=this._self._c||t;return e("div",{staticClass:"wrapper"},[this.showSwiper?e("swiper",{attrs:{options:this.swiperOption}},[this._l(this.list,function(t){return e("swiper-slide",{key:t.movie_id},[e("img",{staticClass:"swiper-img",attrs:{src:t.huge_pic}})])}),this._v(" "),e("div",{staticClass:"swiper-pagination",attrs:{slot:"pagination"},slot:"pagination"})],2):this._e()],1)},staticRenderFns:[]};var g=s("VU/8")(p,f,!1,function(t){s("TVJn")},"data-v-75943bfd",null).exports,_={name:"Listc",props:{list:Array},data:function(){return{}}},C={render:function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",{staticClass:"list-wrapper"},t._l(t.list,function(e){return s("div",{key:e.movie_id,staticClass:"item-wrapper"},[s("router-link",{attrs:{to:"/detail/"+e.movie_id}},[s("div",{staticClass:"item"},[s("div",{staticClass:"item-top"},[s("img",{staticClass:"item-img",attrs:{src:e.cover_pic}})]),t._v(" "),s("div",{staticClass:"item-middle"},[s("div",{staticClass:"item-title"},[t._v(t._s(e.name))]),t._v(" "),s("div",{staticClass:"item-score"},[t._v(t._s(e.douban_score))])]),t._v(" "),s("div",{staticClass:"item-bottom"},[s("div",{staticClass:"item-desc"},[t._v(t._s(e.classification))]),t._v(" "),s("div",{staticClass:"item-comment"},[s("div",{staticClass:"iconfont comment-icon"},[t._v("")]),t._v(" "),s("div",{staticClass:"item-comment-num"},[t._v("\n              "+t._s(e.comment_count)+"\n            ")])])])])])],1)}),0)},staticRenderFns:[]};var w=s("VU/8")(_,C,!1,function(t){s("1/2E")},"data-v-4b4de58d",null).exports,S={name:"HomeSideBar",props:{show:Boolean,list:Array,name:String},components:{Avatar:d},methods:{quit:function(){this.$emit("sidebar"),this.$store.commit("changeUser",{username:"未登录",userStatus:!1}),r.a.post("/api/usr/logout").then(function(){console.log("logout success")})},login:function(){this.$store.state.userStatus||this.$emit("userbox")},handleLinkClick:function(t){var e=t.target.id;if("1"===e)this.$router.go(0);else if("2"===e){if(!this.$store.state.userStatus)return void this.$emit("userbox");this.$router.push("/my")}}}},x={render:function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",{staticClass:"wrapper"},[s("div",{directives:[{name:"show",rawName:"v-show",value:t.show,expression:"show"}],staticClass:"sidebar"},[t._m(0),t._v(" "),s("div",{staticClass:"user-info",on:{click:t.login}},[this.$store.state.userStatus?s("avatar",{staticClass:"avatar",attrs:{imgUrl:"static/avatar.jpeg"}}):s("div",[s("div",{staticClass:"iconfont user-icon"},[t._v("\n          \n        ")])]),t._v(" "),s("div",{staticClass:"user-name"},[t._v(t._s(this.$store.state.username))])],1),t._v(" "),t._l(t.list,function(e){return s("div",{key:e.id,staticClass:"link-item",style:{background:e.color},attrs:{id:e.id},on:{click:t.handleLinkClick}},[s("span",{staticClass:"iconfont icons",domProps:{innerHTML:t._s(e.icon)}}),t._v("\n      "+t._s(e.name)+"\n    ")])}),t._v(" "),this.$store.state.userStatus?s("div",{staticClass:"link-item",style:{background:"#6f599c"},on:{click:t.quit}},[s("span",{staticClass:"iconfont icons",domProps:{innerHTML:t._s("&#xe617;")}}),t._v("\n        注销\n    ")]):t._e()],2),t._v(" "),s("div",{directives:[{name:"show",rawName:"v-show",value:t.show,expression:"show"}],staticClass:"cover",on:{click:function(e){return t.$emit("sidebar")}}})])},staticRenderFns:[function(){var t=this.$createElement,e=this._self._c||t;return e("div",{staticClass:"web-info"},[e("div",{staticClass:"web-name"},[this._v("\n        影推\n      ")])])}]};var b=s("VU/8")(S,x,!1,function(t){s("IIuS")},"data-v-589fa9ea",null).exports,k={name:"HomeTiles",data:function(){return{list:[{id:1,color:"#FE4C40",name:"全部电影"},{id:2,color:"#fdb933",name:"排行榜"},{id:3,color:"#228fbd",name:"随便看看"},{id:4,color:"#008573",name:"我的收藏"}]}},methods:{getRandomOne:function(){r.a.get("/api/randomOne").then(this.getRandomSucc)},getRandomSucc:function(t){var e=(t=t.data).data.movie_id;this.$router.push("/detail/"+e)},handleTileClick:function(t){var e=t.target.id;if("1"===e)this.$router.push("/all");else if("2"===e)this.$router.push("/top");else if("3"===e)this.getRandomOne();else if("4"===e){if(!this.$store.state.userStatus)return void this.$emit("userbox");this.$router.push("/my")}}}},$={render:function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",{staticClass:"tile-wrapper"},t._l(t.list,function(e){return s("div",{key:e.id,staticClass:"item",style:{background:e.color},attrs:{id:e.id},on:{click:t.handleTileClick}},[t._v("\n    "+t._s(e.name)+"\n  ")])}),0)},staticRenderFns:[]};var L=s("VU/8")(k,$,!1,function(t){s("YVww")},"data-v-5d11d6ad",null).exports,y=s("TCmZ"),U=s.n(y),N={name:"User",props:{show:Boolean},data:function(){return{login:!0,username:"",password:"",repeat:"",usernameLimit:/^\w{6,16}$/,passwordLimit:/^\w{6,16}$/,usernameOk:!0,passwordOk:!0,repeatOk:!0}},methods:{userLoginSucc:function(){this.$emit("userbox"),this.$store.commit("changeUser",{username:this.username,userStatus:!0})},userLoginCheck:function(t){200===(t=t.data).code?this.userLoginSucc():alert(t.data.error_msg),console.log(t.data.error_msg)},userLogin:function(){if(this.usernameOk&&this.passwordOk&&this.username&&this.password){var t={login_name:this.username,login_pwd:this.password};r.a.post("/api/usr/login",U.a.stringify(t)).then(this.userLoginCheck)}else alert("用户名以及密码必须是6-16位的数字字母下划线！")},userRegSucc:function(){this.login=!0},userRegCheck:function(t){200===(t=t.data).code?this.userRegSucc():alert("注册失败")},userReg:function(){this.usernameOk&&this.passwordOk&&this.username&&this.password?this.repeat===this.password?r.a.post("/api/usr/reg",U.a.stringify({login_name:this.username,login_pwd:this.password,login_pwd2:this.repeat})).then(this.userRegCheck):alert("两次输入密码不一致！"):alert("用户名以及密码必须是6-16位的数字字母下划线！")},usernameCheck:function(){this.usernameOk=!!this.usernameLimit.exec(this.username)},passwordCheck:function(){this.passwordOk=!!this.passwordLimit.exec(this.password)},repeatCheck:function(){this.repeatOk=!(this.repeat!==this.password)}}},D={render:function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",{staticClass:"wrapper"},[s("div",{directives:[{name:"show",rawName:"v-show",value:t.show,expression:"show"}],staticClass:"user"},[s("div",{staticClass:"switch border-bottom"},[s("div",{staticClass:"login",class:{active:t.login},on:{click:function(e){t.login=!0}}},[t._v("\n        登录\n      ")]),t._v(" "),s("div",{staticClass:"reg",class:{active:!t.login},on:{click:function(e){t.login=!1}}},[t._v("\n        注册\n      ")])]),t._v(" "),s("div",{staticClass:"form"},[s("div",{staticClass:"username"},[t._v("\n        账号：\n        "),s("input",{directives:[{name:"model",rawName:"v-model",value:t.username,expression:"username"}],staticClass:"input",class:{inputError:!t.usernameOk},attrs:{type:"text",placeholder:"请输入用户名"},domProps:{value:t.username},on:{blur:t.usernameCheck,input:function(e){e.target.composing||(t.username=e.target.value)}}})]),t._v(" "),s("div",{staticClass:"password"},[t._v("\n        密码：\n        "),s("input",{directives:[{name:"model",rawName:"v-model",value:t.password,expression:"password"}],staticClass:"input",class:{inputError:!t.passwordOk},attrs:{type:"password",placeholder:"请输入密码"},domProps:{value:t.password},on:{blur:t.passwordCheck,input:function(e){e.target.composing||(t.password=e.target.value)}}})]),t._v(" "),t.login?t._e():s("div",{staticClass:"repeat"},[t._v("\n        确认：\n        "),s("input",{directives:[{name:"model",rawName:"v-model",value:t.repeat,expression:"repeat"}],staticClass:"input",class:{inputError:!t.repeatOk},attrs:{type:"password",placeholder:"请重新输入密码"},domProps:{value:t.repeat},on:{blur:t.repeatCheck,input:function(e){e.target.composing||(t.repeat=e.target.value)}}})]),t._v(" "),t.login?s("button",{staticClass:"btn",on:{click:t.userLogin}},[t._v("登录")]):s("button",{staticClass:"btn",on:{click:t.userReg}},[t._v("注册")])])]),t._v(" "),s("div",{directives:[{name:"show",rawName:"v-show",value:t.show,expression:"show"}],staticClass:"cover",on:{click:function(e){return t.$emit("userbox")}}})])},staticRenderFns:[]};var B=s("VU/8")(N,D,!1,function(t){s("LeWD")},"data-v-5fd2176c",null).exports,I={render:function(){var t=this.$createElement;return(this._self._c||t)("transition",[this._t("default")],2)},staticRenderFns:[]};var R={name:"Home",components:{HomeHeader:h,HomeSwiper:g,HomeList:w,HomeSideBar:b,HomeTiles:L,HomeUser:B,FadeAnimation:s("VU/8")({name:"FadeAnimation"},I,!1,function(t){s("x36r")},"data-v-c75e7cf6",null).exports},data:function(){return{SideBar:!1,UserBox:!1,name:"Mokia",movieList:[],SwiperList:[{movie_id:1,huge_pic:"./static/swiper/1.jpg"},{movie_id:2,huge_pic:"static/swiper/2.jpg"},{movie_id:3,huge_pic:"static/swiper/3.jpg"},{movie_id:4,huge_pic:"static/swiper/4.jpg"},{movie_id:5,huge_pic:"static/swiper/5.jpg"}],LinkList:[{id:1,color:"#7fb80e",name:"首页",icon:"&#xe608;"},{id:2,color:"#f3715c",name:"我的收藏",icon:"&#xe61b;"},{id:3,color:"#404040",name:"历史记录",icon:"&#xe604;"},{id:4,color:"#5875AD",name:"个人资料",icon:"&#xe636;"}]}},methods:{getMovieList:function(){r.a.get("/api/allClass").then(this.getListSucc)},getListSucc:function(t){t=t.data,this.movieList=t.data.movieList},toggleSideBar:function(){this.SideBar=!this.SideBar,this.UserBox=!1},toggleUserBox:function(){this.UserBox=!this.UserBox,this.SideBar=!1}},mounted:function(){this.getMovieList()}},E={render:function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",[s("home-header",{on:{sidebar:t.toggleSideBar,userbox:t.toggleUserBox}}),t._v(" "),s("home-swiper",{attrs:{list:t.SwiperList}}),t._v(" "),s("home-tiles",{on:{userbox:t.toggleUserBox}}),t._v(" "),s("home-list",{attrs:{list:t.movieList}}),t._v(" "),s("home-side-bar",{attrs:{show:t.SideBar,name:t.name,list:t.LinkList},on:{sidebar:t.toggleSideBar,userbox:t.toggleUserBox}}),t._v(" "),s("home-user",{attrs:{show:t.UserBox},on:{userbox:t.toggleUserBox}})],1)},staticRenderFns:[]};var M=s("VU/8")(R,E,!1,function(t){s("4byl")},"data-v-e796f296",null).exports,O=s("fZjL"),T=s.n(O),V={name:"Header",props:{title:String},methods:{handleIconClick:function(){this.$router.go(-1)}}},F={render:function(){var t=this.$createElement,e=this._self._c||t;return e("div",{staticClass:"header"},[e("div",{staticClass:"iconfont back-icon",on:{click:this.handleIconClick}},[this._v("")]),this._v(" "),e("div",{staticClass:"title"},[this._v(this._s(this.title))])])},staticRenderFns:[]};var A=s("VU/8")(V,F,!1,function(t){s("5Gq2")},"data-v-419e6514",null).exports,H={name:"Movie",props:{movieData:Object},mounted:function(){}},j={render:function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",{staticClass:"movie border-bottom"},[s("div",{staticClass:"movie-img"},[s("div",{staticClass:"img-wrapper"},[s("img",{staticClass:"inner-img",attrs:{src:t.movieData.cover_pic}}),t._v(" "),s("div",{staticClass:"movie-score"},[t._v(t._s(t.movieData.douban_score))])])]),t._v(" "),s("div",{staticClass:"movie-info"},[s("div",{staticClass:"movie-title"},[s("div",{staticClass:"movie-name"},[t._v("\n        "+t._s(t.movieData.name)+"\n        "),s("span",{staticClass:"movie-year"},[t._v("("+t._s((t.movieData.pub_date||"").split(" ")[3])+")")])])]),t._v(" "),s("div",{staticClass:"movie-type"},[s("span",{staticClass:"item-title"},[t._v("类型：")]),t._v(t._s(t.movieData.classification))]),t._v(" "),s("div",{staticClass:"movie-area"},[s("span",{staticClass:"item-title"},[t._v("地区：")]),t._v(t._s(t.movieData.area))]),t._v(" "),s("div",{staticClass:"movie-actors"},[s("span",{staticClass:"item-title"},[t._v("主演：")]),t._v(t._s(t.movieData.actors))]),t._v(" "),s("div",{staticClass:"movie-director"},[s("span",{staticClass:"item-title"},[t._v("导演：")]),t._v(t._s(t.movieData.director))])])])},staticRenderFns:[]};var P=s("VU/8")(H,j,!1,function(t){s("e3ah")},"data-v-3f1cad92",null).exports,q={name:"Description",props:{desc:String}},X={render:function(){var t=this.$createElement,e=this._self._c||t;return e("div",{staticClass:"container border-bottom"},[e("div",{staticClass:"top"},[this._v("剧情简介")]),this._v(" "),e("div",{staticClass:"desc"},[this._v(this._s(this.desc))])])},staticRenderFns:[]};var z=s("VU/8")(q,X,!1,function(t){s("21cN")},"data-v-50b92fa8",null).exports,W={name:"CommentItem",props:{content:Object,id:String},components:{Avatar:d},data:function(){return{timer:null}},methods:{touchStart:function(){var t=this,e=this;clearTimeout(this.timer),this.timer=setTimeout(function(){t.$store.state.userStatus&&t.$store.state.username===t.content.nickname&&e.$emit("delete",t.id,t.content.time)},600)},touchEnd:function(){clearTimeout(this.timer)},touchMove:function(){clearTimeout(this.timer)}}},Z={render:function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",{staticClass:"item",on:{touchstart:t.touchStart,touchmove:t.touchMove,touchend:t.touchEnd}},[s("div",{staticClass:"user"},[s("avatar",{attrs:{imgUrl:t.content.head_pic}}),t._v(" "),s("div",{staticClass:"username"},[t._v(t._s(t.content.nickname))])],1),t._v(" "),s("div",{staticClass:"comment"},[t._v(t._s(t.content.content))])])},staticRenderFns:[]};var G=s("VU/8")(W,Z,!1,function(t){s("fWLR")},"data-v-788cce20",null).exports,Y={name:"Comment",props:{list:Object},components:{CommentItem:G},methods:{deleteComment:function(t,e){this.$emit("delete",t,e)}}},J={render:function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",{staticClass:"container border-bottom"},[s("div",{staticClass:"top"},[t._v("评论 ("+t._s(Object.keys(t.list).length)+")")]),t._v(" "),t._l(t.list,function(e,i){return s("comment-item",{key:i,attrs:{content:e,id:i},on:{delete:t.deleteComment}})})],2)},staticRenderFns:[]};var K=s("VU/8")(Y,J,!1,function(t){s("KXX2")},"data-v-fc688486",null).exports,Q={name:"Bottom",props:{stared:Number},data:function(){return{text:""}},methods:{handleBtnClick:function(){this.$store.state.userStatus?this.text&&(this.$emit("newComment",this.text),this.text=""):this.$emit("userbox")},toggleStar:function(){this.$store.state.userStatus?this.$emit("star"):this.$emit("userbox")}}},tt={render:function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",{staticClass:"bottom"},[s("div",{staticClass:"star",on:{click:t.toggleStar}},[t.stared?s("div",{staticClass:"iconfont icon-star"},[t._v("")]):s("div",{staticClass:"iconfont icon-star"},[t._v("")])]),t._v(" "),s("div",{staticClass:"comment"},[s("div",{staticClass:"input"},[s("input",{directives:[{name:"model",rawName:"v-model",value:t.text,expression:"text"}],staticClass:"input-box",attrs:{type:"text",placeholder:"说点儿什么吧"},domProps:{value:t.text},on:{input:function(e){e.target.composing||(t.text=e.target.value)}}})]),t._v(" "),s("button",{staticClass:"btn",on:{click:t.handleBtnClick}},[t._v("提交")])])])},staticRenderFns:[]};var et={name:"Detail",components:{DetailHeader:A,DetailMovie:P,DetailDescription:z,DetailComment:K,DetailBottom:s("VU/8")(Q,tt,!1,function(t){s("nZBw")},"data-v-59466845",null).exports,User:B},data:function(){return{show:!1,movieObj:{},stared:0,list:{}}},methods:{getDetailInfo:function(){r.a.get("/api/movieInfo/"+this.$route.params.id).then(this.getDataSucc)},getDataSucc:function(t){t=t.data,this.movieObj=t.data,this.stared=t.data.stared},getCommentInfo:function(){r.a.get("/api/getComment/"+this.$route.params.id).then(this.getCommentSucc)},getCommentSucc:function(t){t=t.data,this.list=t.data.commentList},addNewComment:function(t){var e={nickname:this.$store.state.username,head_pic:"static/avatar.jpeg",content:t},s=T()(this.list).length;this.$set(this.list,String(s),e),r.a.post("/api/postUpComment",U.a.stringify({movie_id:this.$route.params.id,commentContent:t})).then(function(t){})},toggleUserBox:function(){this.show=!this.show},addStar:function(){r.a.post("/api/usr/addLove/"+this.$route.params.id).then(function(){console.log("star success")})},deleteStar:function(){r.a.post("/api/usr/deleteMyLove/"+this.$route.params.id).then(function(){console.log("star success")})},handleStar:function(){this.stared?this.deleteStar():this.addStar(),this.stared=0===this.stared?1:0},deleteComment:function(t,e){this.$delete(this.list,t),r.a.post("/api/usr/deleteMyComment/"+e).then(function(t){})}},mounted:function(){this.getDetailInfo(),this.getCommentInfo()}},st={render:function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",[s("detail-header",{attrs:{title:"影推"}}),t._v(" "),s("detail-movie",{attrs:{movieData:t.movieObj}}),t._v(" "),s("detail-description",{attrs:{desc:t.movieObj.description}}),t._v(" "),s("detail-comment",{attrs:{list:t.list},on:{delete:t.deleteComment}}),t._v(" "),s("detail-bottom",{attrs:{stared:t.stared},on:{newComment:t.addNewComment,userbox:t.toggleUserBox,star:t.handleStar}}),t._v(" "),s("user",{attrs:{show:t.show},on:{userbox:t.toggleUserBox}})],1)},staticRenderFns:[]};var it=s("VU/8")(et,st,!1,function(t){s("T729")},"data-v-0423d32b",null).exports,at={name:"MyMovie",components:{MyHeader:A,MyList:w},data:function(){return{movieList:[]}},methods:{getMyLove:function(){r.a.get("/api/usr/myLove").then(this.getLoveSucc)},getLoveSucc:function(t){t=t.data,this.movieList=t.data}},mounted:function(){this.getMyLove()}},nt={render:function(){var t=this.$createElement,e=this._self._c||t;return e("div",[e("my-header",{attrs:{title:"我的收藏"}}),this._v(" "),e("my-list",{staticClass:"movie-list",attrs:{list:this.movieList}})],1)},staticRenderFns:[]};var ot=s("VU/8")(at,nt,!1,function(t){s("qD/T")},"data-v-5e589d9a",null).exports,rt={name:"Top",components:{MyHeader:A,MyList:w},data:function(){return{movieList:[]}},methods:{getMovieList:function(){r.a.get("/api/allClass").then(this.getListSucc)},getListSucc:function(t){t=t.data,this.movieList=t.data.movieList},toggleSideBar:function(){this.SideBar=!this.SideBar,this.UserBox=!1},toggleUserBox:function(){this.UserBox=!this.UserBox,this.SideBar=!1}},mounted:function(){this.getMovieList()}},ct={render:function(){var t=this.$createElement,e=this._self._c||t;return e("div",[e("my-header",{attrs:{title:"排行榜"}}),this._v(" "),e("my-list",{staticClass:"movie-list",attrs:{list:this.movieList}})],1)},staticRenderFns:[]};var lt=s("VU/8")(rt,ct,!1,function(t){s("Nlao")},"data-v-58d64237",null).exports,ut={name:"Choose",props:{title:String,list:Array},data:function(){return{chooseIndex:0}},methods:{handleItemClick:function(t){var e=t.target.dataset.name;this.chooseIndex=t.target.id,this.$emit("choose",e)}}},dt={render:function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",{staticClass:"container border-bottom"},[s("ul",{staticClass:"choose"},[s("li",{key:0,staticClass:"title item",class:{active:0==t.chooseIndex},attrs:{id:0,"data-name":""},on:{click:t.handleItemClick}},[t._v("\n      "+t._s(t.title)+"\n    ")]),t._v(" "),t._l(t.list,function(e,i){return s("li",{key:i+1,staticClass:"item",class:{active:t.chooseIndex==i+1},attrs:{"data-name":e,id:i+1},on:{click:t.handleItemClick}},[t._v("\n      "+t._s(e)+"\n    ")])})],2)])},staticRenderFns:[]};var mt={name:"AllMovie",components:{AllHeader:A,AllList:w,AllChoose:s("VU/8")(ut,dt,!1,function(t){s("6GzY")},"data-v-46ede3fe",null).exports},data:function(){return{className:"",areaName:"",movieList:[],classNames:[],areaNames:[]}},methods:{getDetailInfo:function(){var t={};this.className&&(t.class=this.className),this.areaName&&(t.area=this.areaName),0===T()(t).length?r.a.get("/api/allClass").then(this.getDataSucc):r.a.get("/api/allClass",{params:t}).then(this.getDataSucc)},getDataSucc:function(t){t=t.data,this.movieList=t.data.movieList},classChange:function(t){this.className=t},areaChange:function(t){this.areaName=t},getClassName:function(){r.a.get("/api/static/classNames").then(this.getClassSucc)},getClassSucc:function(t){t=t.data,this.classNames=t.data.classNames},getAreaName:function(){r.a.get("/api/static/areaNames").then(this.getAreaSucc)},getAreaSucc:function(t){t=t.data,this.areaNames=t.data.areaNames}},watch:{className:function(){this.getDetailInfo()},areaName:function(){this.getDetailInfo()}},mounted:function(){this.getDetailInfo(),this.getClassName(),this.getAreaName()}},vt={render:function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",[s("all-header",{attrs:{title:"全部电影"}}),t._v(" "),s("all-choose",{staticClass:"choose",attrs:{title:"全部分类",list:t.classNames},on:{choose:t.classChange}}),t._v(" "),s("all-choose",{attrs:{title:"全部地区",list:t.areaNames},on:{choose:t.areaChange}}),t._v(" "),s("all-list",{staticClass:"movie-list",attrs:{list:t.movieList}})],1)},staticRenderFns:[]};var ht=s("VU/8")(mt,vt,!1,function(t){s("2/Xu")},"data-v-5914d582",null).exports;i.default.use(c.a);var pt=new c.a({routes:[{path:"/",name:"Home",component:M},{path:"/detail/:id",name:"Detail",component:it},{path:"/my",name:"MyMovie",component:ot},{path:"/top",name:"Top",component:lt},{path:"/all",name:"All",component:ht}],scrollBehavior:function(t,e,s){return{x:0,y:0}}}),ft=s("iDdd"),gt=s.n(ft),_t=s("ZaBw"),Ct=s.n(_t),wt=s("kciL");i.default.use(wt.a);var St=localStorage.getItem("username")||"未登录",xt=localStorage.getItem("userStatus")||!1,bt=new wt.a.Store({state:{username:St,userStatus:xt},mutations:{changeUser:function(t,e){t.username=e.username,t.userStatus=e.userStatus,localStorage.setItem("username",e.username),localStorage.setItem("userStatus",e.userStatus),e.userStatus||(localStorage.removeItem("username"),localStorage.removeItem("userStatus"))}}});s("9n10"),s("M6Sr"),s("TzC8"),s("S6Il");i.default.prototype.$axios=r.a,r.a.defaults.baseURL="/api",i.default.config.productionTip=!1,gt.a.attach(document.body),i.default.use(Ct.a),r.a.defaults.headers.post["Content-Type"]="application/x-www-form-urlencoded",new i.default({el:"#app",router:pt,store:bt,components:{App:n},template:"<App/>"})},Nlao:function(t,e){},S6Il:function(t,e){},T729:function(t,e){},TVJn:function(t,e){},TzC8:function(t,e){},XcuN:function(t,e){},YVww:function(t,e){},cqTP:function(t,e){},e3ah:function(t,e){},fWLR:function(t,e){},nZBw:function(t,e){},"qD/T":function(t,e){},wlhz:function(t,e){},x36r:function(t,e){}},["NHnr"]);