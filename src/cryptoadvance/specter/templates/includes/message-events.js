/** functions to include in a module to show errors **/
/** this redefines the functions?
function showError(msg){
    let event = new CustomEvent('errormsg', { detail: { message: msg } });
    document.dispatchEvent(event);
}
function Specter.common.showNotification(msg){
    let event = new CustomEvent('notification', { detail: { message: msg } });
    document.dispatchEvent(event);
}
**/