<?php
/**
 * Dredge Host client area menu tweaks.
 *
 * Upload to: /includes/hooks/dredge_navbar.php
 * on the server behind my.dredgehost.com. WHMCS loads every file in
 * includes/hooks automatically; delete the file to undo.
 *
 * - "Network Status" opens the status page on dredgehost.com, so there's one status page.
 * - The empty Knowledgebase is removed from the menu.
 */

use WHMCS\View\Menu\Item as MenuItem;

if (!defined('WHMCS')) {
    die('This file cannot be accessed directly');
}

add_hook('ClientAreaPrimaryNavbar', 1, function (MenuItem $primaryNavbar) {
    $statusPage = 'https://dredgehost.com/status.html';

    // Logged out: top-level items
    if (!is_null($item = $primaryNavbar->getChild('Network Status'))) {
        $item->setUri($statusPage);
    }
    if (!is_null($primaryNavbar->getChild('Knowledgebase'))) {
        $primaryNavbar->removeChild('Knowledgebase');
    }

    // Logged in: the same items sit under Support
    if (!is_null($support = $primaryNavbar->getChild('Support'))) {
        if (!is_null($item = $support->getChild('Network Status'))) {
            $item->setUri($statusPage);
        }
        if (!is_null($support->getChild('Knowledgebase'))) {
            $support->removeChild('Knowledgebase');
        }
    }
});
