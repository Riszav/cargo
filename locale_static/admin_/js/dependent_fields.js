django.jQuery(document).ready(function() {
    django.jQuery("#id_mark").change(function() {
        var markId = django.jQuery(this).val();
        var modelSelect = django.jQuery("#id_model");
        
        // Очищаем текущий список моделей
        modelSelect.empty();
        
        if (markId) {
            // Делаем AJAX запрос для получения списка моделей
            django.jQuery.ajax({
                url: "/admin/catalog/get-models/",
                data: {
                    'mark_id': markId
                },
                dataType: 'json',
                success: function(data) {
                    // Добавляем пустую опцию
                    modelSelect.append(new Option('--------', ''));
                    
                    // Добавляем полученные модели в выпадающий список
                    data.forEach(function(item) {
                        modelSelect.append(new Option(item.name, item.id));
                    });
                }
            });
        }
    });
}); 