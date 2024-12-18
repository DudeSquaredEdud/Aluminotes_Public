/**
 * Adds functionality to tabs
 * @param tabs a string list of each tab's ID.
 * NOTE: The display contents of a tab must be the tab's id, appended with "_contents"
 * EX: tab_input and tab_input_contents
 * @method activate activates a tab
 */
class TabSwitch {
  constructor(tabs) {
    this.tabs = tabs;
  }
  activate(selected_tab) {
    if (!document.getElementById(selected_tab).className.includes('active')) {
      for (let tab in this.tabs) {
        tab = this.tabs[tab];
        document.getElementById(tab).className = document
          .getElementById(tab)
          .className.replace(' active', '');
        document.getElementById(tab + '_contents').style.display = 'none';
      }
      document.getElementById(selected_tab + '_contents').style.display = 'block';
      document.getElementById(selected_tab).className += ' active';
    }
  }
}
