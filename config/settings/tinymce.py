TINYMCE_JS_URL = 'libs/tinymce/tinymce.min.js'

TINYMCE_DEFAULT_CONFIG = {
    'theme': 'silver',
    'height': '500px',
    'branding': False,
    'width': '110%',
    'menubar': 'file edit view insert format tools table help',
    'plugins': 'advlist autolink lists link image charmap print preview anchor searchreplace visualblocks code '
    'fullscreen insertdatetime media table paste code help wordcount spellchecker',
    'toolbar': 'undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft '
    'aligncenter alignright alignjustify | outdent indent |  numlist bullist checklist | forecolor '
    'backcolor casechange permanentpen formatpainter removeformat | pagebreak | charmap emoticons | '
    'fullscreen  preview save print | insertfile image media pageembed template link anchor codesample | '
    'a11ycheck ltr rtl | showcomments addcomment code',
    'custom_undo_redo_levels': 100,
    'language': 'uz', 
    'image_title': 'true',
    'automatic_uploads': 'true',
    'file_picker_types': 'image',
    'relative_urls': False,
    'remove_script_host': False,
    'convert_urls': True,
    
    'file_picker_callback': '''
        function(cb, value, meta) {
            const input = document.createElement('input');
            input.setAttribute('type', 'file');
            input.setAttribute('accept', 'image/*');
            
            input.addEventListener('change', (e) => {
                const file = e.target.files[0];
                
                const formData = new FormData();
                formData.append('file', file);
                
                fetch('/api/tinymce-upload/', {
                    method: 'POST',
                    body: formData,
                    credentials: 'include'
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    cb(data.location, { title: file.name });
                })
                .catch(error => {
                    console.error('Error uploading file:', error);
                    alert('Upload failed: ' + error.message);
                });
            });
            
            input.click();
        }
    '''
}