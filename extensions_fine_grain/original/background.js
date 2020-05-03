'use strict';

chrome.runtime.onInstalled.addListener(function() {
  chrome.cookies.set({url: 'http://example.com/', name: 'cookie', value: 'test'});

  chrome.cookies.getAll({domain: 'example.com'}, function(cookies) {
    console.log(cookies);
  });
});