apex.StromTree = {
   'tree_block': '#arhive',
   'storm_api_url': 'http://127.0.0.1:5000/search/',
   'archive_url': 'http://en-arc-01:8080/?6&cardId=',
   'opened': false
};
apex.StromTree.click_document = function(document_id){
    window.open(apex.StromTree['archive_url']+document_id,'_blank');
    return false;
};
apex.jQuery( document ).ready( function() {
    var $ = apex.jQuery,
        archive_handler = $(apex.StromTree['tree_block']),
        content_handler = archive_handler.find('div.uRegionContent'),
        center_id_handler = $('#MSNCENTRE_ID');

    archive_handler.find('a.uRegionControl').click(function(){
        var self = $(this),
            center_id = center_id_handler.val(),
            tree_id = 'tree_'+center_id;
        content_handler.empty();

        if(!apex.StromTree['opened']){
            content_handler.html('<div id="'+tree_id+'">Загрузка...</div>');
            $.ajax({
                url: apex.StromTree['storm_api_url']+center_id,
                method: 'GET',
                dataType: 'json'
            }).done(function(data){
                apex.StromTree['opened'] = true;
                apex.widget.tree.init(tree_id, apex.widget.tree.cTreeTypes, data['data'], "default", center_id,"S","");
            });
        }else{
            apex.StromTree['opened'] = false;
        }
    });
});