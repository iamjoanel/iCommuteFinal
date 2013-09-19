(function ($) {
    var defaults, w,
		_responsiveTable = 'responsiveTable',
		_container = 'Container',
		_overflow = 'overflow',
		_static = 'Static',
		_overflowContainer = _overflow + _container,
		_staticContainer = 'static' + _container,
		_nthChild = 'nth-child',
		_divClass = '<div class="',
		isResponsive = false,
        responsiveContainers,
		tableWidth,
		tableStatic, tableStaticRow, rowCells, rowCellsClone, uiHint;

    $.fn.responsiveTable = function (options) {
        w = $(window);
        defaults = {
            staticColumns: 1,
            scrollRight: true,
            scrollHintEnabled: true,
            scrollHintDuration: 2000
        };
        options = $.extend(defaults, options);

        function setupScrollHint(table, offset) {
            // Display a hint to the user that the table contents are scrollable
            var uid = _responsiveTable + 'UiHint';
            if ($('#' + uid).length == 0) {
                uiHint = $('<div id="' + uid + '">&lt;&lt;  Scroll table left and right  &gt;&gt;</div>');
                $('body').prepend(uiHint);
                var ht = w.height() / 2;
                if (offset.top > 0 && table.height() > 0) {
                    ht = offset.top + (table.height() * 0.4);
                }
                uiHint.css({
                    "position": "absolute",
                    "z-index": 1000000,
                    "padding": "0.5em",
                    "background-color": "#888",
                    "color": "#eee",
                    "font-size": "1.1em",
                    "border-radius": "0.6em"
                }).css({
                    "top": ht,
                    "left": (w.width() / 2) - (uiHint.width() / 2)
                });
            }
            setTimeout('$("#' + uid + '").hide();', options.scrollHintDuration);
        }

        function getResponsiveContainers(table) {
            var oc = table.parent();
            return { rtc: oc.parent(), oc: oc, sc: oc.parent().find('.' + _staticContainer) };
        }

        function resizeResponsiveTable(table) {
            // Resize the overflow container
            responsiveContainers = getResponsiveContainers(table);
            // Set the overflow container width
            responsiveContainers.oc.width(responsiveContainers.rtc.innerWidth() - responsiveContainers.sc.outerWidth() - 1);
            // Scroll right so the right hand side is displayed by default
            if (options.scrollRight) {
                responsiveContainers.oc.scrollLeft(table.width());
            }
        }

        function setResponsiveTable(table) {
            if (!table.parent().hasClass(_overflowContainer)) {
                console.log('applying');
                var tos = table.offset();
                table.wrap(_divClass + _responsiveTable + _container + '" style="' + _overflow + ':hidden;"/>');
                tableStatic = $('<table/>');

                // Copy table attributes
                $.each(table[0].attributes, function (index, a) {
                    if (a.name !== 'id') {
                        tableStatic.attr(a.name, a.value);
                    }
                });
                tableStatic.addClass(_responsiveTable + _static)
					.css('border-right', 'ridge')
					.width(0);
                // Select direct child rows only, we don't want rows from nested tables
                table.find('>tr,>tbody>tr').each(function (i, element) {
                    tableStaticRow = $('<tr/>');
                    // Set the height to the calculated height of the original row, the natural height of the cloned cells may be different
                    tableStaticRow.outerHeight($(element).outerHeight());
                    // Copy row attributes
                    $.each($(element)[0].attributes, function (index, a) {
                        if (a.name !== 'id') {
                            tableStaticRow.attr(a.name, a.value);
                        }
                    });
                    for (i = 0; i <= options.staticColumns; i++) {
                        // Clone the cells for configured number of columns
                        rowCells = $(element).find('>th:' + _nthChild + '(' + i + '),>td:' + _nthChild + '(' + i + ')');
                        rowCellsClone = rowCells.clone();
                        rowCells.css('display', 'none');
                        tableStaticRow.append(rowCellsClone);
                        tableStatic.append(tableStaticRow);
                    }
                });
                table.before(tableStatic);

                table.wrap(_divClass + _overflowContainer + '" style="float:left;' + _overflow + ':scroll;' + _overflow + '-y:hidden;"/>');
                tableStatic.wrap(_divClass + _staticContainer + '" style="float:left;"/>');

                if (options.scrollHintEnabled) {
                    setupScrollHint(table, tos);
                }
            }

            resizeResponsiveTable(table);

            // Check the positions and resize if alignment is not correct, this has to be done twice in some cases as jQuery does not return the correct width for the overflow container
            responsiveContainers = getResponsiveContainers(table);
            if (responsiveContainers.sc.position().top < responsiveContainers.oc.position().top) {
                resizeResponsiveTable(table);
                resizeResponsiveTable(table);
            }
        }

        function unsetResponsiveTable(table) {
            if (table.parent().hasClass(_overflowContainer)) {
                $('.' + _staticContainer).remove();
                table.unwrap().unwrap().find('tr').each(function (i, element) {
                    for (i = 0; i <= options.staticColumns; i++) {
                        $(element).find('th:' + _nthChild + '(' + i + '),td:' + _nthChild + '(' + i + ')').css('display', '');
                    }
                });
            }
        }

        // Detect overflow by checking the table width against that of its parent tree
        function setupResponsiveTable(table) {
            tableWidth = table.width();
            if (table.parent().hasClass(_overflowContainer)) {
                tableWidth += $('.' + _staticContainer).width();
            }

            isResponsive = false;
            table.parents().each(function () {
                if (!$(this).hasClass(_overflowContainer)
					&& tableWidth > $(this).width()
				) {
                    isResponsive = true;

                    // break out of each
                    return (false);
                }
            });

            // Set or unset the responsive table
            if (isResponsive) {
                setResponsiveTable(table);
            } else {
                unsetResponsiveTable(table);
            }
        }

        return this.each(function () {
            var $this = $(this);
            if (!$this.hasClass(_responsiveTable + _static)) {
                w.on('resize orientationchange', function () {
                    setupResponsiveTable($this);
                });
                setupResponsiveTable($this);
            }
        });
    };
})(jQuery); 