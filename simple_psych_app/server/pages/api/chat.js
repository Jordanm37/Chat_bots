"use strict";
/*
 * ATTENTION: An "eval-source-map" devtool has been used.
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file with attached SourceMaps in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
(() => {
var exports = {};
exports.id = "pages/api/chat";
exports.ids = ["pages/api/chat"];
exports.modules = {

/***/ "(api)/./pages/api/chat.js":
/*!***************************!*\
  !*** ./pages/api/chat.js ***!
  \***************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   \"default\": () => (/* export default binding */ __WEBPACK_DEFAULT_EXPORT__)\n/* harmony export */ });\n/* harmony default export */ async function __WEBPACK_DEFAULT_EXPORT__(req, res) {\n    const response = await fetch(process.env.LCC_ENDPOINT_URL, {\n        method: \"POST\",\n        headers: {\n            \"Content-Type\": \"application/json\",\n            \"X-Api-Key\": process.env.LCC_TOKEN\n        },\n        body: JSON.stringify({\n            question: req.body.question,\n            history: req.body.history\n        })\n    });\n    const data = await response.json();\n    res.status(200).json({\n        result: data\n    });\n}\n//# sourceURL=[module]\n//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiKGFwaSkvLi9wYWdlcy9hcGkvY2hhdC5qcy5qcyIsIm1hcHBpbmdzIjoiOzs7O0FBQUEsNkJBQWUsMENBQWdCQSxHQUFHLEVBQUVDLEdBQUcsRUFBRTtJQUV2QyxNQUFNQyxXQUFXLE1BQU1DLE1BQU1DLFFBQVFDLEdBQUcsQ0FBQ0MsZ0JBQWdCLEVBQUU7UUFDekRDLFFBQVE7UUFDUkMsU0FBUztZQUNQLGdCQUFnQjtZQUNoQixhQUFhSixRQUFRQyxHQUFHLENBQUNJLFNBQVM7UUFDcEM7UUFDQUMsTUFBTUMsS0FBS0MsU0FBUyxDQUFDO1lBQ25CQyxVQUFVYixJQUFJVSxJQUFJLENBQUNHLFFBQVE7WUFDM0JDLFNBQVNkLElBQUlVLElBQUksQ0FBQ0ksT0FBTztRQUMzQjtJQUNGO0lBRUUsTUFBTUMsT0FBTyxNQUFNYixTQUFTYyxJQUFJO0lBRWhDZixJQUFJZ0IsTUFBTSxDQUFDLEtBQUtELElBQUksQ0FBQztRQUFFRSxRQUFRSDtJQUFLO0FBQ3hDLENBQUMiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9sYW5nY2hhaW4tY2hhdC8uL3BhZ2VzL2FwaS9jaGF0LmpzPzFjNDkiXSwic291cmNlc0NvbnRlbnQiOlsiZXhwb3J0IGRlZmF1bHQgYXN5bmMgZnVuY3Rpb24gKHJlcSwgcmVzKSB7XHJcblxyXG4gIGNvbnN0IHJlc3BvbnNlID0gYXdhaXQgZmV0Y2gocHJvY2Vzcy5lbnYuTENDX0VORFBPSU5UX1VSTCwge1xyXG4gICAgbWV0aG9kOiBcIlBPU1RcIixcclxuICAgIGhlYWRlcnM6IHtcclxuICAgICAgXCJDb250ZW50LVR5cGVcIjogXCJhcHBsaWNhdGlvbi9qc29uXCIsXHJcbiAgICAgIFwiWC1BcGktS2V5XCI6IHByb2Nlc3MuZW52LkxDQ19UT0tFTlxyXG4gICAgfSxcclxuICAgIGJvZHk6IEpTT04uc3RyaW5naWZ5KHtcclxuICAgICAgcXVlc3Rpb246IHJlcS5ib2R5LnF1ZXN0aW9uLFxyXG4gICAgICBoaXN0b3J5OiByZXEuYm9keS5oaXN0b3J5XHJcbiAgICB9KSxcclxuICB9KTtcclxuXHJcbiAgICBjb25zdCBkYXRhID0gYXdhaXQgcmVzcG9uc2UuanNvbigpO1xyXG5cclxuICAgIHJlcy5zdGF0dXMoMjAwKS5qc29uKHsgcmVzdWx0OiBkYXRhIH0pXHJcbn0iXSwibmFtZXMiOlsicmVxIiwicmVzIiwicmVzcG9uc2UiLCJmZXRjaCIsInByb2Nlc3MiLCJlbnYiLCJMQ0NfRU5EUE9JTlRfVVJMIiwibWV0aG9kIiwiaGVhZGVycyIsIkxDQ19UT0tFTiIsImJvZHkiLCJKU09OIiwic3RyaW5naWZ5IiwicXVlc3Rpb24iLCJoaXN0b3J5IiwiZGF0YSIsImpzb24iLCJzdGF0dXMiLCJyZXN1bHQiXSwic291cmNlUm9vdCI6IiJ9\n//# sourceURL=webpack-internal:///(api)/./pages/api/chat.js\n");

/***/ })

};
;

// load runtime
var __webpack_require__ = require("../../webpack-api-runtime.js");
__webpack_require__.C(exports);
var __webpack_exec__ = (moduleId) => (__webpack_require__(__webpack_require__.s = moduleId))
var __webpack_exports__ = (__webpack_exec__("(api)/./pages/api/chat.js"));
module.exports = __webpack_exports__;

})();