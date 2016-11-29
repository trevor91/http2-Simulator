$(function () {
        var submit_form = function () {
            if (nc.elcheck(".page-loader-wrapper")) {
                $(".page-loader-wrapper").fadeIn(10);
            }
            var inputURL = encodeURIComponent($('input[name="url"]').val());
            var origin = location.href;

            $.getJSON($SCRIPT_ROOT + '/', {
                url: inputURL
            }, function (data) {
                if (nc.elcheck(".page-loader-wrapper")) {
                    $(".page-loader-wrapper").fadeOut(10);
                }
                if (data.notice != 'scraping') {
                    $("#notice").html("");
                    $("#notice").append('<div class="inputStyle"><div id="myflew" style="display:inline-flex;"><h3 id="h3url" style="color:greenyellow;">' + inputURL + '&nbsp;</h3></div></div>');
                    $("#myflew").append('<h3 id="istested">is tested</h3>');
                    $("#notice").append('<h3 id="h3notice">' + data.notice + '</h3>');
                } else {
                    if (nc.elcheck(".page-loader-wrapper")) {
                        $(".page-loader-wrapper").fadeIn(10);
                    }
                    window.location.href = origin + 'scraping?url=' + data.url;
                    // $.ajax({
                    //     type: "POST",
                    //     url: "snapshot.py",
                    //     data: {
                    //         url: "http://www.naver.com",
                    //         name: "naver.com"
                    //     }
                    // }).done(function (o) {
                    //     window.location.replace('https://www.h2perf.com/scraping?url=' + data.url);
                    // });
                }
            });
        }
        $('#btsubmit').bind('click', submit_form);

        $('input[name="url"]').bind('keydown', function (e) {
            var url = $('input[name="url"]').val();
            if (e.keyCode == 13) {
                if (url !== "") {
                    submit_form()
                } else {
                    e.preventDefault()
                }
            }

        });
        return false;
    }
);


