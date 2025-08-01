/*
 Highcharts JS v8.0.4 (2020-03-10)

 Old IE (v6, v7, v8) module for Highcharts v6+.

 (c) 2010-2019 Highsoft AS
 Author: Torstein Honsi

 License: www.highcharts.com/license
*/
(function (e) {
    "object" === typeof module && module.exports ? (e["default"] = e, module.exports = e) : "function" === typeof define && define.amd ? define("highcharts/modules/oldie", ["highcharts"], function (n) {
        e(n);
        e.Highcharts = n;
        return e
    }) : e("undefined" !== typeof Highcharts ? Highcharts : void 0)
})(function (e) {
    function n(m, e, g, n) {
        m.hasOwnProperty(e) || (m[e] = n.apply(null, g))
    }

    e = e ? e._modules : {};
    n(e, "modules/oldie.src.js", [e["parts/Globals.js"], e["parts/Color.js"], e["parts/Utilities.js"]], function (m, e, g) {
        var n = e.parse, k = g.addEvent,
            C = g.createElement, x = g.css, F = g.defined, G = g.discardElement, H = g.erase, z = g.extend,
            A = g.extendClass, O = g.isArray, L = g.isNumber, D = g.isObject;
        e = g.merge;
        var P = g.offset, t = g.pick, r = g.pInt, Q = g.uniqueKey, M = m.Chart, u = m.deg2rad, h = m.doc, N = m.noop,
            E = m.svg, y = m.SVGElement, v = m.SVGRenderer, w = m.win;
        m.getOptions().global.VMLRadialGradientURL = "http://code.highcharts.com/8.0.4/gfx/vml-radial-gradient.png";
        h && !h.defaultView && (m.getStyle = g.getStyle = function (a, b) {
            var c = {width: "clientWidth", height: "clientHeight"}[b];
            if (a.style[b]) return r(a.style[b]);
            "opacity" === b && (b = "filter");
            if (c) return a.style.zoom = 1, Math.max(a[c] - 2 * g.getStyle(a, "padding"), 0);
            a = a.currentStyle[b.replace(/\-(\w)/g, function (a, b) {
                return b.toUpperCase()
            })];
            "filter" === b && (a = a.replace(/alpha\(opacity=([0-9]+)\)/, function (a, b) {
                return b / 100
            }));
            return "" === a ? 1 : r(a)
        });
        E || (k(y, "afterInit", function () {
            "text" === this.element.nodeName && this.css({position: "absolute"})
        }), m.Pointer.prototype.normalize = function (a, b) {
            a = a || w.event;
            a.target || (a.target = a.srcElement);
            b || (this.chartPosition = b = P(this.chart.container));
            return z(a, {chartX: Math.round(Math.max(a.x, a.clientX - b.left)), chartY: Math.round(a.y)})
        }, M.prototype.ieSanitizeSVG = function (a) {
            return a = a.replace(/<IMG /g, "<image ").replace(/<(\/?)TITLE>/g, "<$1title>").replace(/height=([^" ]+)/g, 'height="$1"').replace(/width=([^" ]+)/g, 'width="$1"').replace(/hc-svg-href="([^"]+)">/g, 'xlink:href="$1"/>').replace(/ id=([^" >]+)/g, ' id="$1"').replace(/class=([^" >]+)/g, 'class="$1"').replace(/ transform /g, " ").replace(/:(path|rect)/g, "$1").replace(/style="([^"]+)"/g,
                function (a) {
                    return a.toLowerCase()
                })
        }, M.prototype.isReadyToRender = function () {
            var a = this;
            return E || w != w.top || "complete" === h.readyState ? !0 : (h.attachEvent("onreadystatechange", function () {
                h.detachEvent("onreadystatechange", a.firstRender);
                "complete" === h.readyState && a.firstRender()
            }), !1)
        }, h.createElementNS || (h.createElementNS = function (a, b) {
            return h.createElement(b)
        }), m.addEventListenerPolyfill = function (a, b) {
            function c(a) {
                a.target = a.srcElement || w;
                b.call(d, a)
            }

            var d = this;
            d.attachEvent && (d.hcEventsIE || (d.hcEventsIE =
                {}), b.hcKey || (b.hcKey = Q()), d.hcEventsIE[b.hcKey] = c, d.attachEvent("on" + a, c))
        }, m.removeEventListenerPolyfill = function (a, b) {
            this.detachEvent && (b = this.hcEventsIE[b.hcKey], this.detachEvent("on" + a, b))
        }, k = {
            docMode8: h && 8 === h.documentMode, init: function (a, b) {
                var c = ["<", b, ' filled="f" stroked="f"'], d = ["position: ", "absolute", ";"], f = "div" === b;
                ("shape" === b || f) && d.push("left:0;top:0;width:1px;height:1px;");
                d.push("visibility: ", f ? "hidden" : "visible");
                c.push(' style="', d.join(""), '"/>');
                b && (c = f || "span" === b || "img" ===
                b ? c.join("") : a.prepVML(c), this.element = C(c));
                this.renderer = a
            }, add: function (a) {
                var b = this.renderer, c = this.element, d = b.box, f = a && a.inverted;
                d = a ? a.element || a : d;
                a && (this.parentGroup = a);
                f && b.invertChild(c, d);
                d.appendChild(c);
                this.added = !0;
                this.alignOnAdd && !this.deferUpdateTransform && this.updateTransform();
                if (this.onAdd) this.onAdd();
                this.className && this.attr("class", this.className);
                return this
            }, updateTransform: y.prototype.htmlUpdateTransform, setSpanRotation: function () {
                var a = this.rotation, b = Math.cos(a * u),
                    c = Math.sin(a * u);
                x(this.element, {filter: a ? ["progid:DXImageTransform.Microsoft.Matrix(M11=", b, ", M12=", -c, ", M21=", c, ", M22=", b, ", sizingMethod='auto expand')"].join("") : "none"})
            }, getSpanCorrection: function (a, b, c, d, f) {
                var p = d ? Math.cos(d * u) : 1, e = d ? Math.sin(d * u) : 0,
                    I = t(this.elemHeight, this.element.offsetHeight);
                this.xCorr = 0 > p && -a;
                this.yCorr = 0 > e && -I;
                var l = 0 > p * e;
                this.xCorr += e * b * (l ? 1 - c : c);
                this.yCorr -= p * b * (d ? l ? c : 1 - c : 1);
                f && "left" !== f && (this.xCorr -= a * c * (0 > p ? -1 : 1), d && (this.yCorr -= I * c * (0 > e ? -1 : 1)), x(this.element,
                    {textAlign: f}))
            }, pathToVML: function (a) {
                for (var b = a.length, c = []; b--;) L(a[b]) ? c[b] = Math.round(10 * a[b]) - 5 : "Z" === a[b] ? c[b] = "x" : (c[b] = a[b], !a.isArc || "wa" !== a[b] && "at" !== a[b] || (c[b + 5] === c[b + 7] && (c[b + 7] += a[b + 7] > a[b + 5] ? 1 : -1), c[b + 6] === c[b + 8] && (c[b + 8] += a[b + 8] > a[b + 6] ? 1 : -1)));
                return c.join(" ") || "x"
            }, clip: function (a) {
                var b = this;
                if (a) {
                    var c = a.members;
                    H(c, b);
                    c.push(b);
                    b.destroyClip = function () {
                        H(c, b)
                    };
                    a = a.getCSS(b)
                } else b.destroyClip && b.destroyClip(), a = {clip: b.docMode8 ? "inherit" : "rect(auto)"};
                return b.css(a)
            }, css: y.prototype.htmlCss,
            safeRemoveChild: function (a) {
                a.parentNode && G(a)
            }, destroy: function () {
                this.destroyClip && this.destroyClip();
                return y.prototype.destroy.apply(this)
            }, on: function (a, b) {
                this.element["on" + a] = function () {
                    var a = w.event;
                    a.target = a.srcElement;
                    b(a)
                };
                return this
            }, cutOffPath: function (a, b) {
                a = a.split(/[ ,]/);
                var c = a.length;
                if (9 === c || 11 === c) a[c - 4] = a[c - 2] = r(a[c - 2]) - 10 * b;
                return a.join(" ")
            }, shadow: function (a, b, c) {
                var d = [], f, p = this.element, e = this.renderer, I = p.style, l = p.path;
                l && "string" !== typeof l.value && (l = "x");
                var m = l;
                if (a) {
                    var g = t(a.width, 3);
                    var q = (a.opacity || .15) / g;
                    for (f = 1; 3 >= f; f++) {
                        var h = 2 * g + 1 - 2 * f;
                        c && (m = this.cutOffPath(l.value, h + .5));
                        var k = ['<shape isShadow="true" strokeweight="', h, '" filled="false" path="', m, '" coordsize="10 10" style="', p.style.cssText, '" />'];
                        var n = C(e.prepVML(k), null, {
                            left: r(I.left) + t(a.offsetX, 1),
                            top: r(I.top) + t(a.offsetY, 1)
                        });
                        c && (n.cutOff = h + 1);
                        k = ['<stroke color="', a.color || "#000000", '" opacity="', q * f, '"/>'];
                        C(e.prepVML(k), null, null, n);
                        b ? b.element.appendChild(n) : p.parentNode.insertBefore(n,
                            p);
                        d.push(n)
                    }
                    this.shadows = d
                }
                return this
            }, updateShadows: N, setAttr: function (a, b) {
                this.docMode8 ? this.element[a] = b : this.element.setAttribute(a, b)
            }, getAttr: function (a) {
                return this.docMode8 ? this.element[a] : this.element.getAttribute(a)
            }, classSetter: function (a) {
                (this.added ? this.element : this).className = a
            }, dashstyleSetter: function (a, b, c) {
                (c.getElementsByTagName("stroke")[0] || C(this.renderer.prepVML(["<stroke/>"]), null, null, c))[b] = a || "solid";
                this[b] = a
            }, dSetter: function (a, b, c) {
                var d = this.shadows;
                a = a || [];
                this.d =
                    a.join && a.join(" ");
                c.path = a = this.pathToVML(a);
                if (d) for (c = d.length; c--;) d[c].path = d[c].cutOff ? this.cutOffPath(a, d[c].cutOff) : a;
                this.setAttr(b, a)
            }, fillSetter: function (a, b, c) {
                var d = c.nodeName;
                "SPAN" === d ? c.style.color = a : "IMG" !== d && (c.filled = "none" !== a, this.setAttr("fillcolor", this.renderer.color(a, c, b, this)))
            }, "fill-opacitySetter": function (a, b, c) {
                C(this.renderer.prepVML(["<", b.split("-")[0], ' opacity="', a, '"/>']), null, null, c)
            }, opacitySetter: N, rotationSetter: function (a, b, c) {
                c = c.style;
                this[b] = c[b] = a;
                c.left =
                    -Math.round(Math.sin(a * u) + 1) + "px";
                c.top = Math.round(Math.cos(a * u)) + "px"
            }, strokeSetter: function (a, b, c) {
                this.setAttr("strokecolor", this.renderer.color(a, c, b, this))
            }, "stroke-widthSetter": function (a, b, c) {
                c.stroked = !!a;
                this[b] = a;
                L(a) && (a += "px");
                this.setAttr("strokeweight", a)
            }, titleSetter: function (a, b) {
                this.setAttr(b, a)
            }, visibilitySetter: function (a, b, c) {
                "inherit" === a && (a = "visible");
                this.shadows && this.shadows.forEach(function (c) {
                    c.style[b] = a
                });
                "DIV" === c.nodeName && (a = "hidden" === a ? "-999em" : 0, this.docMode8 ||
                (c.style[b] = a ? "visible" : "hidden"), b = "top");
                c.style[b] = a
            }, xSetter: function (a, b, c) {
                this[b] = a;
                "x" === b ? b = "left" : "y" === b && (b = "top");
                this.updateClipping ? (this[b] = a, this.updateClipping()) : c.style[b] = a
            }, zIndexSetter: function (a, b, c) {
                c.style[b] = a
            }, fillGetter: function () {
                return this.getAttr("fillcolor") || ""
            }, strokeGetter: function () {
                return this.getAttr("strokecolor") || ""
            }, classGetter: function () {
                return this.getAttr("className") || ""
            }
        }, k["stroke-opacitySetter"] = k["fill-opacitySetter"], m.VMLElement = k = A(y, k), k.prototype.ySetter =
            k.prototype.widthSetter = k.prototype.heightSetter = k.prototype.xSetter, k = {
            Element: k, isIE8: -1 < w.navigator.userAgent.indexOf("MSIE 8.0"), init: function (a, b, c) {
                this.alignedObjects = [];
                var d = this.createElement("div").css({position: "relative"});
                var f = d.element;
                a.appendChild(d.element);
                this.isVML = !0;
                this.box = f;
                this.boxWrapper = d;
                this.gradients = {};
                this.cache = {};
                this.cacheKeys = [];
                this.imgCount = 0;
                this.setSize(b, c, !1);
                if (!h.namespaces.hcv) {
                    h.namespaces.add("hcv", "urn:schemas-microsoft-com:vml");
                    try {
                        h.createStyleSheet().cssText =
                            "hcv\\:fill, hcv\\:path, hcv\\:shape, hcv\\:stroke{ behavior:url(#default#VML); display: inline-block; } "
                    } catch (p) {
                        h.styleSheets[0].cssText += "hcv\\:fill, hcv\\:path, hcv\\:shape, hcv\\:stroke{ behavior:url(#default#VML); display: inline-block; } "
                    }
                }
            }, isHidden: function () {
                return !this.box.offsetWidth
            }, clipRect: function (a, b, c, d) {
                var f = this.createElement(), e = D(a);
                return z(f, {
                    members: [],
                    count: 0,
                    left: (e ? a.x : a) + 1,
                    top: (e ? a.y : b) + 1,
                    width: (e ? a.width : c) - 1,
                    height: (e ? a.height : d) - 1,
                    getCSS: function (a) {
                        var b = a.element,
                            c = b.nodeName, d = a.inverted, f = this.top - ("shape" === c ? b.offsetTop : 0),
                            e = this.left;
                        b = e + this.width;
                        var p = f + this.height;
                        f = {clip: "rect(" + Math.round(d ? e : f) + "px," + Math.round(d ? p : b) + "px," + Math.round(d ? b : p) + "px," + Math.round(d ? f : e) + "px)"};
                        !d && a.docMode8 && "DIV" === c && z(f, {width: b + "px", height: p + "px"});
                        return f
                    },
                    updateClipping: function () {
                        f.members.forEach(function (a) {
                            a.element && a.css(f.getCSS(a))
                        })
                    }
                })
            }, color: function (a, b, c, d) {
                var f = this, e = /^rgba/, g, h, l = "none";
                a && a.linearGradient ? h = "gradient" : a && a.radialGradient && (h =
                    "pattern");
                if (h) {
                    var k, r, q = a.linearGradient || a.radialGradient, u, v, w, y, x = "";
                    a = a.stops;
                    var z = [], A = function () {
                        g = ['<fill colors="' + z.join(",") + '" opacity="', v, '" o:opacity2="', u, '" type="', h, '" ', x, 'focus="100%" method="any" />'];
                        C(f.prepVML(g), null, null, b)
                    };
                    var t = a[0];
                    var D = a[a.length - 1];
                    0 < t[0] && a.unshift([0, t[1]]);
                    1 > D[0] && a.push([1, D[1]]);
                    a.forEach(function (a, b) {
                        e.test(a[1]) ? (J = n(a[1]), k = J.get("rgb"), r = J.get("a")) : (k = a[1], r = 1);
                        z.push(100 * a[0] + "% " + k);
                        b ? (v = r, w = k) : (u = r, y = k)
                    });
                    if ("fill" === c) if ("gradient" ===
                        h) c = q.x1 || q[0] || 0, a = q.y1 || q[1] || 0, t = q.x2 || q[2] || 0, q = q.y2 || q[3] || 0, x = 'angle="' + (90 - 180 * Math.atan((q - a) / (t - c)) / Math.PI) + '"', A(); else {
                        l = q.r;
                        var E = 2 * l, F = 2 * l, G = q.cx, H = q.cy, K = b.radialReference, B;
                        l = function () {
                            K && (B = d.getBBox(), G += (K[0] - B.x) / B.width - .5, H += (K[1] - B.y) / B.height - .5, E *= K[2] / B.width, F *= K[2] / B.height);
                            x = 'src="' + m.getOptions().global.VMLRadialGradientURL + '" size="' + E + "," + F + '" origin="0.5,0.5" position="' + G + "," + H + '" color2="' + y + '" ';
                            A()
                        };
                        d.added ? l() : d.onAdd = l;
                        l = w
                    } else l = k
                } else if (e.test(a) && "IMG" !==
                    b.tagName) {
                    var J = n(a);
                    d[c + "-opacitySetter"](J.get("a"), c, b);
                    l = J.get("rgb")
                } else l = b.getElementsByTagName(c), l.length && (l[0].opacity = 1, l[0].type = "solid"), l = a;
                return l
            }, prepVML: function (a) {
                var b = this.isIE8;
                a = a.join("");
                b ? (a = a.replace("/>", ' xmlns="urn:schemas-microsoft-com:vml" />'), a = -1 === a.indexOf('style="') ? a.replace("/>", ' style="display:inline-block;behavior:url(#default#VML);" />') : a.replace('style="', 'style="display:inline-block;behavior:url(#default#VML);')) : a = a.replace("<", "<hcv:");
                return a
            },
            text: v.prototype.html, path: function (a) {
                var b = {coordsize: "10 10"};
                O(a) ? b.d = a : D(a) && z(b, a);
                return this.createElement("shape").attr(b)
            }, circle: function (a, b, c) {
                var d = this.symbol("circle");
                D(a) && (c = a.r, b = a.y, a = a.x);
                d.isCircle = !0;
                d.r = c;
                return d.attr({x: a, y: b})
            }, g: function (a) {
                var b;
                a && (b = {className: "highcharts-" + a, "class": "highcharts-" + a});
                return this.createElement("div").attr(b)
            }, image: function (a, b, c, d, f) {
                var e = this.createElement("img").attr({src: a});
                1 < arguments.length && e.attr({x: b, y: c, width: d, height: f});
                return e
            }, createElement: function (a) {
                return "rect" === a ? this.symbol(a) : v.prototype.createElement.call(this, a)
            }, invertChild: function (a, b) {
                var c = this;
                b = b.style;
                var d = "IMG" === a.tagName && a.style;
                x(a, {
                    flip: "x",
                    left: r(b.width) - (d ? r(d.top) : 1),
                    top: r(b.height) - (d ? r(d.left) : 1),
                    rotation: -90
                });
                [].forEach.call(a.childNodes, function (b) {
                    c.invertChild(b, a)
                })
            }, symbols: {
                arc: function (a, b, c, d, f) {
                    var e = f.start, h = f.end, g = f.r || c || d;
                    c = f.innerR;
                    d = Math.cos(e);
                    var l = Math.sin(e), k = Math.cos(h), m = Math.sin(h);
                    if (0 === h - e) return ["x"];
                    e = ["wa", a - g, b - g, a + g, b + g, a + g * d, b + g * l, a + g * k, b + g * m];
                    f.open && !c && e.push("e", "M", a, b);
                    e.push("at", a - c, b - c, a + c, b + c, a + c * k, b + c * m, a + c * d, b + c * l, "x", "e");
                    e.isArc = !0;
                    return e
                }, circle: function (a, b, c, d, e) {
                    e && F(e.r) && (c = d = 2 * e.r);
                    e && e.isCircle && (a -= c / 2, b -= d / 2);
                    return ["wa", a, b, a + c, b + d, a + c, b + d / 2, a + c, b + d / 2, "e"]
                }, rect: function (a, b, c, d, e) {
                    return v.prototype.symbols[F(e) && e.r ? "callout" : "square"].call(0, a, b, c, d, e)
                }
            }
        }, m.VMLRenderer = A = function () {
            this.init.apply(this, arguments)
        }, A.prototype = e(v.prototype, k), m.Renderer = A);
        v.prototype.getSpanWidth =
            function (a, b) {
                var c = a.getBBox(!0).width;
                !E && this.forExport && (c = this.measureSpanWidth(b.firstChild.data, a.styles));
                return c
            };
        v.prototype.measureSpanWidth = function (a, b) {
            var c = h.createElement("span");
            a = h.createTextNode(a);
            c.appendChild(a);
            x(c, b);
            this.box.appendChild(c);
            b = c.offsetWidth;
            G(c);
            return b
        }
    });
    n(e, "masters/modules/oldie.src.js", [], function () {
    })
});
//# sourceMappingURL=oldie.js.map