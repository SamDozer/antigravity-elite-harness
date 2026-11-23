import { contextBridge, ipcRenderer } from 'electron';

export interface DesktopAPI {
  getAppVersion: () => Promise<string>;
  openFileDialog: () => Promise<string | null>;
}

const api: DesktopAPI = {
  getAppVersion: () => ipcRenderer.invoke('app:get-version'),
  openFileDialog: () => ipcRenderer.invoke('dialog:open-file'),
};

contextBridge.exposeInMainWorld('desktopAPI', Object.freeze(api));
