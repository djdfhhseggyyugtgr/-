(async () => {
  const ids = [
    "geckolib",
    "animated_java",
    "colour_gradient_generator",
    "plaster",
    "texture_stitcher",
    "grayscale_preview",
    "bone_view",
    "expand_bone_timeline",
    "true_mirror",
    "duplicate_renamer",
    "optimize"
  ];
  await Plugins.loading_promise;
  const results = {};
  for (const id of ids) {
    const plugin = Plugins.all.find((p) => p.id === id);
    if (!plugin) { results[id] = "not found in the plugin store"; continue; }
    if (plugin.installed) { results[id] = "already installed " + plugin.version; continue; }
    const installable = plugin.isInstallable();
    if (installable !== true) { results[id] = "not installable: " + installable; continue; }
    try {
      await plugin.install();
      results[id] = plugin.installed ? "installed " + plugin.version : "install did not complete";
    } catch (err) {
      results[id] = "error: " + String(err);
    }
  }
  return { blockbench: Blockbench.version, results };
})()
