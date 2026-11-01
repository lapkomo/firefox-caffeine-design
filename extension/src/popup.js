const browserApi = typeof browser !== 'undefined' ? browser : chrome;

async function loadSettings() {
  const { settings } = await browserApi.storage.local.get('settings');
  return settings || { enabled: false, helperInstalled: false, status: 'not-configured' };
}

async function updatePopup() {
  const settings = await loadSettings();
  const checkbox = document.getElementById('enabled');
  const status = document.getElementById('status');

  checkbox.checked = Boolean(settings.enabled);
  status.textContent = settings.helperInstalled ? `状態: ${settings.status}` : '未設定: ヘルパーの確認が必要です';
}

document.addEventListener('DOMContentLoaded', async () => {
  const checkbox = document.getElementById('enabled');
  const status = document.getElementById('status');
  const button = document.getElementById('setup-button');

  await updatePopup();

  checkbox.addEventListener('change', async (event) => {
    const enabled = event.target.checked;
    const { settings } = await browserApi.storage.local.get('settings');
    const next = {
      ...(settings || {}),
      enabled,
      status: enabled ? 'enabled' : 'disabled',
    };
    await browserApi.storage.local.set({ settings: next });
    status.textContent = `状態: ${next.status}`;
  });

  button.addEventListener('click', async () => {
    const result = await browserApi.runtime.sendMessage({ type: 'setup-check' });
    const nextSettings = result && result.settings ? result.settings : { helperInstalled: false, status: 'helper-missing' };

    await browserApi.storage.local.set({ settings: nextSettings });
    status.textContent = nextSettings.helperInstalled ? `状態: ${nextSettings.status}` : '未設定: ヘルパーの確認が必要です';
  });
});
