const DEFAULT_STATE = {
  enabled: false,
  helperInstalled: false,
  status: 'not-configured',
};

const browserApi = typeof browser !== 'undefined' ? browser : chrome;

async function ensureState() {
  const stored = await browserApi.storage.local.get('settings');
  const settings = { ...DEFAULT_STATE, ...(stored.settings || {}) };
  await browserApi.storage.local.set({ settings });
  return settings;
}

browserApi.runtime.onInstalled.addListener(async () => {
  const settings = await ensureState();
  console.log('Firefox Caffeine initialized', settings);
});

browserApi.runtime.onStartup.addListener(async () => {
  const settings = await ensureState();
  console.log('Firefox Caffeine startup', settings);
});

browserApi.runtime.onMessage.addListener((message, _sender, sendResponse) => {
  if (message && message.type === 'setup-check') {
    ensureState().then((settings) => {
      sendResponse({ ok: true, settings });
    });
    return true;
  }

  if (message && message.type === 'set-enabled') {
    ensureState().then(async (settings) => {
      settings.enabled = Boolean(message.enabled);
      settings.status = settings.enabled ? 'enabled' : 'disabled';
      await browserApi.storage.local.set({ settings });
      sendResponse({ ok: true, settings });
    });
    return true;
  }

  return false;
});
