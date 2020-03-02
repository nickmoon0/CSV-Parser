import Vue from 'vue'
import Router from 'vue-router'
import { interopDefault } from './utils'

const _0ec0322c = () => interopDefault(import('../pages/accounts.vue' /* webpackChunkName: "pages/accounts" */))
const _6fedf48a = () => interopDefault(import('../pages/createAccount.vue' /* webpackChunkName: "pages/createAccount" */))
const _7fd37f4c = () => interopDefault(import('../pages/enterData.vue' /* webpackChunkName: "pages/enterData" */))
const _0ace6eb1 = () => interopDefault(import('../pages/errors.vue' /* webpackChunkName: "pages/errors" */))
const _1136cda5 = () => interopDefault(import('../pages/home.vue' /* webpackChunkName: "pages/home" */))
const _3387cd93 = () => interopDefault(import('../pages/login.vue' /* webpackChunkName: "pages/login" */))
const _eafa2560 = () => interopDefault(import('../pages/logout.vue' /* webpackChunkName: "pages/logout" */))
const _2d5e8a58 = () => interopDefault(import('../pages/retreiveData.vue' /* webpackChunkName: "pages/retreiveData" */))
const _cc805b72 = () => interopDefault(import('../pages/upload.vue' /* webpackChunkName: "pages/upload" */))
const _69e02a7c = () => interopDefault(import('../pages/index.vue' /* webpackChunkName: "pages/index" */))

Vue.use(Router)

if (process.client) {
  if ('scrollRestoration' in window.history) {
    window.history.scrollRestoration = 'manual'

    // reset scrollRestoration to auto when leaving page, allowing page reload
    // and back-navigation from other pages to use the browser to restore the
    // scrolling position.
    window.addEventListener('beforeunload', () => {
      window.history.scrollRestoration = 'auto'
    })

    // Setting scrollRestoration to manual again when returning to this page.
    window.addEventListener('load', () => {
      window.history.scrollRestoration = 'manual'
    })
  }
}
const scrollBehavior = function (to, from, savedPosition) {
  // if the returned position is falsy or an empty object,
  // will retain current scroll position.
  let position = false

  // if no children detected and scrollToTop is not explicitly disabled
  if (
    to.matched.length < 2 &&
    to.matched.every(r => r.components.default.options.scrollToTop !== false)
  ) {
    // scroll to the top of the page
    position = { x: 0, y: 0 }
  } else if (to.matched.some(r => r.components.default.options.scrollToTop)) {
    // if one of the children has scrollToTop option set to true
    position = { x: 0, y: 0 }
  }

  // savedPosition is only available for popstate navigations (back button)
  if (savedPosition) {
    position = savedPosition
  }

  return new Promise((resolve) => {
    // wait for the out transition to complete (if necessary)
    window.$nuxt.$once('triggerScroll', () => {
      // coords will be used if no selector is provided,
      // or if the selector didn't match any element.
      if (to.hash) {
        let hash = to.hash
        // CSS.escape() is not supported with IE and Edge.
        if (typeof window.CSS !== 'undefined' && typeof window.CSS.escape !== 'undefined') {
          hash = '#' + window.CSS.escape(hash.substr(1))
        }
        try {
          if (document.querySelector(hash)) {
            // scroll to anchor by returning the selector
            position = { selector: hash }
          }
        } catch (e) {
          console.warn('Failed to save scroll position. Please add CSS.escape() polyfill (https://github.com/mathiasbynens/CSS.escape).')
        }
      }
      resolve(position)
    })
  })
}

export function createRouter() {
  return new Router({
    mode: 'history',
    base: decodeURI('/'),
    linkActiveClass: 'nuxt-link-active',
    linkExactActiveClass: 'nuxt-link-exact-active',
    scrollBehavior,

    routes: [{
      path: "/accounts",
      component: _0ec0322c,
      name: "accounts"
    }, {
      path: "/createAccount",
      component: _6fedf48a,
      name: "createAccount"
    }, {
      path: "/enterData",
      component: _7fd37f4c,
      name: "enterData"
    }, {
      path: "/errors",
      component: _0ace6eb1,
      name: "errors"
    }, {
      path: "/home",
      component: _1136cda5,
      name: "home"
    }, {
      path: "/login",
      component: _3387cd93,
      name: "login"
    }, {
      path: "/logout",
      component: _eafa2560,
      name: "logout"
    }, {
      path: "/retreiveData",
      component: _2d5e8a58,
      name: "retreiveData"
    }, {
      path: "/upload",
      component: _cc805b72,
      name: "upload"
    }, {
      path: "/",
      component: _69e02a7c,
      name: "index"
    }],

    fallback: false
  })
}
