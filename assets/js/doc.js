/* 資料ページ共通:スマホ向けの補助機能(JS が動かなくても本文は読めます) */
(function () {
  // 1) 表:各セルに見出し名を付ける(スマホでカード表示にするため)
  document.querySelectorAll("main table").forEach(function (t) {
    var heads = Array.prototype.map.call(t.querySelectorAll("thead th"), function (th) { return th.textContent.trim(); });
    t.querySelectorAll("tbody tr").forEach(function (tr) {
      Array.prototype.forEach.call(tr.children, function (td, i) { if (heads[i]) td.setAttribute("data-label", heads[i]); });
    });
  });

  // 2) 図:タップすると画面いっぱいに拡大(ドラッグ・ピンチで動かせる)
  var box = document.createElement("div");
  box.className = "lightbox";
  box.innerHTML = '<button type="button" class="lightbox-close" aria-label="閉じる">× 閉じる</button><div class="lightbox-body"><img alt=""></div>';
  document.body.appendChild(box);
  var big = box.querySelector("img");
  function close() { box.classList.remove("open"); document.body.classList.remove("no-scroll"); }
  box.addEventListener("click", function (e) { if (e.target !== big) close(); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") close(); });
  document.querySelectorAll(".figure img").forEach(function (img) {
    img.addEventListener("click", function () {
      big.src = img.src; big.alt = img.alt;
      box.classList.add("open"); document.body.classList.add("no-scroll");
    });
  });

  // 3) 「↑ 目次」ボタン:少しスクロールしたら右下に表示
  var toc = document.getElementById("toc");
  if (toc) {
    var a = document.createElement("a");
    a.href = "#toc"; a.className = "to-toc"; a.textContent = "↑ 目次";
    document.body.appendChild(a);
    function onScroll() { a.classList.toggle("show", window.scrollY > 600); }
    window.addEventListener("scroll", onScroll, { passive: true }); onScroll();
  }
})();
