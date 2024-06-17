const mobilemenu = document.getElementById('m-btn');

mobilemenu.addEventListener('click', function() {
    //console.log('togglemenu');
    document.getElementById('menu-list').classList.toggle("show");
    //document.getElementById('languages').classList.remove("lang-expanded");
});

