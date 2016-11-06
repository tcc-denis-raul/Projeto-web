$('.vote label i.fa').on('click mouseover', function(){
    $('.vote label i.fa').removeClass('active');
    var val =$(this).prev('input').val();
    $('.vote label i.fa').each(function(){
        var $input = $(this).prev('input');
        if($input.val() <= val){
            $(this).addClass('active');
        }
    })
    $("#voto").html(val);
});

$('.vote').mouseleave(function(){
    var val = $(this).find('input:checked').val();
    if(val == undefined ){
        $('.vote label i.fa').removeClass('active');
    } else {
        $('.vote label i.fa').each(function(){
            var $input = $(this).prev('input');
            if($input.val() > val){
                $(this).removeClass('active');
            } else {
                $(this).addClass('active');
            }
        });
    }
    $("#voto").html(val);
})
