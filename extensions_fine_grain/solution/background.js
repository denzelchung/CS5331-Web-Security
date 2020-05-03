'use strict';

// Access to cookies APIs that reads cookie values
const CookieReader = {
  get: (details, callback) => {
    chrome.cookies.get(details, callback);
  },

  getAll: (details, callback) => {
    chrome.cookies.getAll(details, callback);
  },

  getAllCookieStores: (details, callback) => {
    chrome.cookies.getAllCookieStores(details, callback);
  },
  
  onChanged: (callback) => {
    chrome.cookies.onChanged.addListener(callback);
  }
}

// Access to cookies APIs that modify cookie values
const CookieWriter = {
  set: (details, callback) => {
    chrome.cookies.set(details, callback);
  },

  remove: (details, callback) => {
    chrome.cookies.remove(details, callback);
  }
}

chrome.runtime.onInstalled.addListener(function() {
  CookieReader.get({url: 'http://example.com/', name: 'cookie'}, function(cookie) {
    console.log(cookie);
  });
  
  CookieReader.onChanged(function(changeInfo) {
    console.log('cookie changed', changeInfo);
  });
  
  CookieWriter.set({url: 'http://example.com/', name: 'cookie', value: 'test'});
});