$(document)
  .on('click', '#add-my-contacts a.btn-delete', function(){
    var
      btn = $(this),
      row = btn.closest('div.control-group'),
      url = btn.attr('href')
    ;

    $.post(url, {}, function(json){
      if (json && json.success) {
        row.fadeOut();
      };
    });

    return false;
  })
  .on('blur', 'input[data-contacts-role=account]', function(){
    var
      $input = $(this),
      updateUrl = $input.data('update-url'),
      $handler
    ;
    if (updateUrl) {
      var data = {
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        'account': $input.val(),
        'type': $('select[data-contacts-role=type][data-update-url="'+updateUrl+'"]').val()
      }
      $hanlder = $.post(updateUrl, data, function(json){
        console.log(json)
        //
      }, 'json')
    }


    return false;
  })
  .on('click', '#add-my-contacts a.btn-create', function(){
    var
      btn = $(this),
      row = btn.closest('div.control-group'),
      url = btn.attr('href'),
      data = {csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()}
    ;
    row.removeClass('error');

    $('span.help-block', row).remove();
    $(':input', row).each(function(i, v){
      var input = $(this);
      data[input.attr('name')] = input.val();
    });

    $.post(url, data, function(json){
      if (json && json.success) {
        var
          newRow = row.clone(false)
        ;
        $('a.btn', newRow)
          .removeClass('btn-create')
          .addClass('btn-delete')
          .removeClass('glyphicon-plus')
          .addClass('glyphicon-minus')
          .attr('href', json.delete_url)
        ;

        newRow.removeClass('dynamic').insertBefore(row).fadeIn();

        $(':input', row).each(function(i,v){
          $(':input:eq('+i+')', newRow).val( $(v).val());
            $(v).val('')
          })
        } else if (! json.success) {
          var
            msg = $('<span class="help-block error">' + json.errors[0] + '</span>').appendTo(row)
          ;
          row.addClass('has-error')
        }
      });
      return false;
    });
  ;