(async () => {
  await Plugins.loading_promise;
  return {
    blockbench: Blockbench.version,
    installed: Plugins.installed.map((p) => ({ id: p.id, version: p.version, source: p.source, disabled: !!p.disabled }))
  };
})()
