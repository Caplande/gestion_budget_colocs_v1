self.addEventListener("install", (e) => {
  console.log("SW installé");
});

self.addEventListener("fetch", (e) => {
  // Pour cette démo on laisse tout passer
  // (plus tard tu mettras du cache offline)
});
