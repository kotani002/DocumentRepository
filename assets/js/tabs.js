/* 資料トップのタブ切り替え(JS が動かない場合は、すべてのパネルがそのまま表示されます) */
(function () {
  var tabs = Array.prototype.slice.call(document.querySelectorAll(".tabs [data-tab]"));
  var panels = Array.prototype.slice.call(document.querySelectorAll(".tab-panel"));
  if (!tabs.length) return;
  document.documentElement.classList.add("has-tabs");
  function show(name) {
    tabs.forEach(function (t) {
      var on = t.getAttribute("data-tab") === name;
      t.setAttribute("aria-selected", on ? "true" : "false");
      t.tabIndex = on ? 0 : -1;
    });
    panels.forEach(function (p) { p.hidden = p.id !== "panel-" + name; });
    try { history.replaceState(null, "", "#" + name); } catch (e) {}
  }
  tabs.forEach(function (t, i) {
    t.addEventListener("click", function () { show(t.getAttribute("data-tab")); });
    t.addEventListener("keydown", function (e) {
      var d = e.key === "ArrowRight" ? 1 : e.key === "ArrowLeft" ? -1 : 0;
      if (!d) return;
      var n = tabs[(i + d + tabs.length) % tabs.length];
      n.focus(); show(n.getAttribute("data-tab"));
    });
  });
  var h = location.hash.replace("#", "");
  show(tabs.some(function (t) { return t.getAttribute("data-tab") === h; }) ? h : tabs[0].getAttribute("data-tab"));
})();
