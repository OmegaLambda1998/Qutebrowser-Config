// ==UserScript==
// @name        Fix Slack Notifications
// @author      Original: bascht (https://github.com/qutebrowser/qutebrowser/issues/5233#issuecomment-614444694)
// @author      Updated: OmegaLambda (https://www.omegalambda.au/)
// @description	Hits the notification button, once
// @version	1.1
// @namespace   https://app.slack.com/
// @match       https://*.slack.com/*
// @match       https://*.slack-edge.com/*
// @run-at      document-idle
// @grant       none
// ==/UserScript==

//
// --- Logging Setup ---
//

// Will be added to all logs, so it's clear which script is logging
const SCRIPTNAME = `fix-slack-notifications`;

// LOGLEVEL is the maximum level of logging which will be printed
//  0: console.error
//  1: console.warn
//  2: console.info
//  3: console.debug
//  4: console.trace
const LOGLEVEL = 4;
const LOGGER = [console.error, console.warn, console.info, console.debug, console.trace];


// Log `message` with priority `level`
function log(level, message) {
    if (LOGLEVEL >= level) {
        LOGGER[level](new Date(), SCRIPTNAME, message);
    }
}

// Log `message` as an error
function error(message) { log(0, message); }

// Log `message` as a warning
function warn(message) { log(1, message); }

// Log `message` as info
function info(message) { log(2, message); }

// Log `message` as a debug message
function debug(message) { log(3, message); }

// Log `message` alongside trace
function trace(message) { log(4, message); }

//
// --- Helper Functions ---
//

//      attemptGetElement(xpath)
//
//  Return the first element matching `xpath`, if any exist
//
//  `xpath`: an xpathExpression which identifies the element of interest
function attemptGetElement(xpath) {
    return document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
}

//      sleep(ms)
//
// Sleep for `ms`
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

//
// --- Script Start ---
//

//      waitForElement(xpath, interval, attempts)
//  
//  Wait until an element exists in the document, then resolve the Promise with the element
//
//  `xpath`: An xpathExpression which identifies the element of interest
//  `interval=500`: Amount of time in ms between attempts
//  `max_attempts=20`: Maximum number of attempts before quitting. If max_attempts < 0 => infinite attempts
async function waitForElement(xpath, interval=500, max_attempts=20) {
    return new Promise((resolve, reject) => {
        let attempt = 1;
        let checkExist = setInterval(function() {
            debug(`Attempt ${attempt}`)

            // See if we've surpassed `max_attempts`
            if (max_attempts >= 0 && attempt >= max_attempts) {
                warn(`After ${attempt} attempts, no element matching ${xpath} was found`);
                clearInterval(checkExist);
                reject(false);
            }

            // Try and get element matching `xpath`
            let element = attemptGetElement(xpath);

            // If we found a matching element, run callback
            if (element) {
                debug(`Found ${element} at ${xpath}`);
                clearInterval(checkExist);
                resolve(element);
            }

            // If we didn't find a matching element, try again after `interval` ms
            attempt++;
        }, interval);
    });
}

//      enableSlackNotifications()
//
//  Wait until slack asks about notifications, then press the `Enable notifications` option
async function enableSlackNotifications() {
    let enable_xpath = "//button[text()='Enable notifications']";

    try {
        let button = await waitForElement(enable_xpath, undefined, -1);
        debug(`Pressing notification button`);
        button.click();
        debug(`Testing if click was successful`);
        await sleep(1000);
        let element = attemptGetElement(enable_xpath) 
        return (element ? false : true);
    } catch (e) {
        return false;
    }
}

//      closeNotificationBanner()
//
//  After enabling notifications, close the banner
async function closeNotificationBanner() {
    let close_xpath = "//button[@data-qa='banner_close_btn']";

    try {
        let button = await waitForElement(close_xpath);
        debug(`Pressing banner close button`);
        button.click();
        debug(`Testing if click was successful`);
        await sleep(1000);
        let element = attemptGetElement(close_xpath) 
        return (element ? false : true);
    } catch (e) {
        return false;
    }
}

// Main (anonymous) script function
(async function () {
    info(`Script Started`);

    info(`Attempting to enable slack notifications`);
    let success = await enableSlackNotifications();
    if (success) {
        info(`Slack notifications enabled`);
        info(`Attempting to close notification banner`);
        success = await closeNotificationBanner();
        if (success) {
            info(`Notification banner closed`);
        } else {
            info(`Could not close notification banner`);
        }
    } else {
        info(`Could not enable slack notifications`);
    }

    info(`Script Finished`);
})();
