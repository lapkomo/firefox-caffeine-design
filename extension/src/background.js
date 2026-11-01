const DEFAULT_STATE = {
  enabled: false,
  helperInstalled: false,
  status: 'not-configured',
};

const NATIVE_HOST_NAME = 'firefox_caffeine';
const browserApi = typeof browser !== 'undefined' ? browser : chrome;

async function ensureState() {
  const stored = await browserApi.storage.local.get('settings');
  const settings = { ...DEFAULT_STATE, ...(stored.settings || {}) };
  await browserApi.storage.local.set({ settings });
  return settings;
}

async function checkHelperAvailability() {
  try {
    const response = await browserApi.runtime.sendNativeMessage(NATIVE_HOST_NAME, {
      action: 'probe',
      timestamp: Date.now(),
    });

    const helperInstalled = Boolean(response && response.status === 'ok');
    const settings = await ensureState();
    const nextSettings = {
      ...settings,
      helperInstalled,
      status: helperInstalled ? 'helper-ready' : 'helper-missing',
    };

    await browserApi.storage.local.set({ settings: nextSettings });
    return { ok: true, settings: nextSettings, response };
  } catch (error) {
    const settings = await ensureState();
    const nextSettings = {
      ...settings,
      helperInstalled: false,
      status: 'helper-missing',
    };

    await browserApi.storage.local.set({ settings: nextSettings });
    return { ok: false, settings: nextSettings, error: String(error) };
  }
}

browserApi.runtime.onInstalled.addListener(async () => {
  const settings = await checkHelperAvailability();
  console.log('Firefox Caffeine initialized', settings);
});

browserApi.runtime.onStartup.addListener(async () => {
  const settings = await checkHelperAvailability();
  console.log('Firefox Caffeine startup', settings);
});

browserApi.runtime.onMessage.addListener((message, _sender, sendResponse) => {
  if (message && message.type === 'setup-check') {
    checkHelperAvailability().then((result) => {
      sendResponse(result);
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
