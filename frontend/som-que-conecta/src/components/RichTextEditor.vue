<template>
  <div class="main-container">
    <div
      ref="editorContainerElement"
      class="editor-container editor-container_classic-editor editor-container_include-style editor-container_include-fullscreen"
    >
      <div class="editor-container__editor">
        <div ref="editorElement">
          <ckeditor 
            v-if="editor && config" 
            :model-value="model-value" 
            :editor="editor"
            :config="config" 
            @update:modelValue="$emit('update:model-value', $event)" 
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
/**
 * This configuration was generated using the CKEditor 5 Builder. You can modify it anytime using this link:
 * https://ckeditor.com/ckeditor-5/builder/?redirect=portal#installation/NoNgNARATAdCMEYKQVBBOArOgLABhwGYRcd0s89Mi0AOYzK2qkAdhB2s1aj2QgCmAO2R4wwBGElix0gLqRaCVjgBGIKBDlA=
 */

import { computed, ref, onMounted } from 'vue';
import { Ckeditor, useCKEditorCloud } from '@ckeditor/ckeditor5-vue';
import articleService from '@/services/articleService';
import api from '@/services/api';

const props = defineProps({
	modelValue: {
		type: String,
		default: ''
	}
});

defineEmits(['update:model-value']);

const LICENSE_KEY = process.env.VUE_APP_CKEDITOR_LICENSE_KEY;

const cloud = useCKEditorCloud({ version: '45.2.0' });

const isLayoutReady = ref(false);

const editor = computed(() => {
	if (!cloud.data.value) {
		return null;
	}
	return cloud.data.value.CKEditor.ClassicEditor;
});

const config = computed(() => {
	if (!isLayoutReady.value || !cloud.data.value) {
		return null;
	}

	const {
		Alignment,
		Autoformat,
		AutoImage,
		Autosave,
		BalloonToolbar,
		BlockQuote,
		Bold,
		Bookmark,
		Code,
		CodeBlock,
		Essentials,
		FontBackgroundColor,
		FontColor,
		FontFamily,
		FontSize,
		Fullscreen,
		GeneralHtmlSupport,
		Heading,
		Highlight,
		HorizontalLine,
		ImageBlock,
		ImageCaption,
		ImageInline,
		ImageInsert,
		ImageInsertViaUrl,
		ImageResize,
		ImageStyle,
		ImageTextAlternative,
		ImageToolbar,
		ImageUpload,
		Indent,
		IndentBlock,
		Italic,
		Link,
		LinkImage,
		List,
		ListProperties,
		MediaEmbed,
		PageBreak,
		Paragraph,
		PasteFromOffice,
		PlainTableOutput,
		RemoveFormat,
		SimpleUploadAdapter,
		SourceEditing,
		SpecialCharacters,
		SpecialCharactersArrows,
		SpecialCharactersCurrency,
		SpecialCharactersEssentials,
		SpecialCharactersLatin,
		SpecialCharactersMathematical,
		SpecialCharactersText,
		Strikethrough,
		Style,
		Subscript,
		Superscript,
		Table,
		TableCaption,
		TableCellProperties,
		TableColumnResize,
		TableLayout,
		TableProperties,
		TableToolbar,
		TextTransformation,
		TodoList,
		Underline
	} = cloud.data.value.CKEditor;

	return {
		toolbar: {
			items: [
				'undo',
				'redo',
				'|',
				'sourceEditing',
				'|',
				'heading',
				'style',
				'|',
				'fontSize',
				'fontFamily',
				'fontColor',
				'fontBackgroundColor',
				'|',
				'bold',
				'italic',
				'underline',
				'|',
				'link',
				'insertImage',
				'insertTable',
				'insertTableLayout',
				'highlight',
				'blockQuote',
				'codeBlock',
				'|',
				'alignment',
				'|',
				'bulletedList',
				'numberedList',
				'todoList',
				'outdent',
				'indent'
			],
			shouldNotGroupWhenFull: true
		},
		plugins: [
			Alignment,
			Autoformat,
			AutoImage,
			Autosave,
			BalloonToolbar,
			BlockQuote,
			Bold,
			Bookmark,
			Code,
			CodeBlock,
			Essentials,
			FontBackgroundColor,
			FontColor,
			FontFamily,
			FontSize,
			Fullscreen,
			GeneralHtmlSupport,
			Heading,
			Highlight,
			HorizontalLine,
			ImageBlock,
			ImageCaption,
			ImageInline,
			ImageInsert,
			ImageInsertViaUrl,
			ImageResize,
			ImageStyle,
			ImageTextAlternative,
			ImageToolbar,
			ImageUpload,
			Indent,
			IndentBlock,
			Italic,
			Link,
			LinkImage,
			List,
			ListProperties,
			MediaEmbed,
			PageBreak,
			Paragraph,
			PasteFromOffice,
			PlainTableOutput,
			RemoveFormat,
			SimpleUploadAdapter,
			SourceEditing,
			SpecialCharacters,
			SpecialCharactersArrows,
			SpecialCharactersCurrency,
			SpecialCharactersEssentials,
			SpecialCharactersLatin,
			SpecialCharactersMathematical,
			SpecialCharactersText,
			Strikethrough,
			Style,
			Subscript,
			Superscript,
			Table,
			TableCaption,
			TableCellProperties,
			TableColumnResize,
			TableLayout,
			TableProperties,
			TableToolbar,
			TextTransformation,
			TodoList,
			Underline
		],
		balloonToolbar: ['bold', 'italic', '|', 'link', 'insertImage', '|', 'bulletedList', 'numberedList'],
		fontFamily: {
			supportAllValues: true
		},
		fontSize: {
			options: [10, 12, 14, 'default', 18, 20, 22],
			supportAllValues: true
		},
		fullscreen: {
			onEnterCallback: container =>
				container.classList.add(
					'editor-container',
					'editor-container_classic-editor',
					'editor-container_include-style',
					'editor-container_include-fullscreen',
					'main-container'
				)
		},
		heading: {
			options: [
				{
					model: 'paragraph',
					title: 'Paragraph',
					class: 'ck-heading_paragraph'
				},
				{
					model: 'heading1',
					view: 'h1',
					title: 'Heading 1',
					class: 'ck-heading_heading1'
				},
				{
					model: 'heading2',
					view: 'h2',
					title: 'Heading 2',
					class: 'ck-heading_heading2'
				},
				{
					model: 'heading3',
					view: 'h3',
					title: 'Heading 3',
					class: 'ck-heading_heading3'
				},
				{
					model: 'heading4',
					view: 'h4',
					title: 'Heading 4',
					class: 'ck-heading_heading4'
				},
				{
					model: 'heading5',
					view: 'h5',
					title: 'Heading 5',
					class: 'ck-heading_heading5'
				},
				{
					model: 'heading6',
					view: 'h6',
					title: 'Heading 6',
					class: 'ck-heading_heading6'
				}
			]
		},
		htmlSupport: {
			allow: [
				{
					name: /^.*$/,
					styles: true,
					attributes: true,
					classes: true
				}
			]
		},
		image: {
			toolbar: [
				'toggleImageCaption',
				'imageTextAlternative',
				'|',
				'imageStyle:inline',
				'imageStyle:wrapText',
				'imageStyle:breakText',
				'|',
				'resizeImage'
			],
			upload: {
				types: ['jpeg', 'png', 'gif', 'bmp', 'webp', 'tiff']
			},
			styles: [
				'alignLeft',
				'alignCenter',
				'alignRight'
			],
			resizeOptions: [
				{
					name: 'imageResize:original',
					value: null,
					label: 'Original'
				},
				{
					name: 'imageResize:50',
					value: '50',
					label: '50%'
				},
				{
					name: 'imageResize:75',
					value: '75',
					label: '75%'
				}
			],
			resizeUnit: '%'
		},
		licenseKey: LICENSE_KEY,
		link: {
			addTargetToExternalLinks: true,
			defaultProtocol: 'https://',
			decorators: {
				toggleDownloadable: {
					mode: 'manual',
					label: 'Downloadable',
					attributes: {
						download: 'file'
					}
				}
			}
		},
		list: {
			properties: {
				styles: true,
				startIndex: true,
				reversed: true
			}
		},
		menuBar: {
			isVisible: true
		},
		placeholder: 'Digite ou cole seu conteúdo aqui!',
		style: {
			definitions: [
				{
					name: 'Article category',
					element: 'h3',
					classes: ['category']
				},
				{
					name: 'Title',
					element: 'h2',
					classes: ['document-title']
				},
				{
					name: 'Subtitle',
					element: 'h3',
					classes: ['document-subtitle']
				},
				{
					name: 'Info box',
					element: 'p',
					classes: ['info-box']
				},
				{
					name: 'CTA Link Primary',
					element: 'a',
					classes: ['button', 'button--green']
				},
				{
					name: 'CTA Link Secondary',
					element: 'a',
					classes: ['button', 'button--black']
				},
				{
					name: 'Marker',
					element: 'span',
					classes: ['marker']
				},
				{
					name: 'Spoiler',
					element: 'span',
					classes: ['spoiler']
				}
			]
		},
		table: {
			contentToolbar: ['tableColumn', 'tableRow', 'mergeTableCells', 'tableProperties', 'tableCellProperties']
		},
		simpleUpload: {
			uploadUrl: `${api.defaults.baseURL}articles/upload-image/`,
			withCredentials: true,
			headers: {
				Authorization: `Bearer ${localStorage.getItem('accessToken')}`
			},
			upload: async (file) => {
				console.log('Iniciando upload...')
				console.log('Arquivo recebido:', file)
				console.log('Tipo do arquivo:', file.type)
				console.log('Tamanho do arquivo:', file.size)

				const uploadUrl = `${api.defaults.baseURL}articles/upload-image/`
				console.log('URL de upload:', uploadUrl)
				console.log('Token de autenticação:', api.defaults.headers.common['Authorization'])

				const formData = new FormData()
				formData.append('upload', file)
				console.log('FormData criado:', formData)

				try {
					const response = await api.post('articles/upload-image/', formData, {
						headers: {
							'Content-Type': 'multipart/form-data',
						},
						withCredentials: true
					})
					console.log('Resposta do servidor:', response.data)
					
					// Retorna o formato esperado pelo CKEditor
					return {
						url: response.data.url,
						uploaded: response.data.uploaded,
						fileName: response.data.fileName,
						error: response.data.error
					}
				} catch (error) {
					console.error('Erro no upload:', error)
					console.error('Detalhes do erro:', {
						response: error.response?.data,
						status: error.response?.status,
						headers: error.response?.headers
					})
					return {
						uploaded: false,
						error: {
							message: error.response?.data?.error?.message || 'Erro ao fazer upload da imagem'
						}
					}
				}
			}
		}
	};
});

onMounted(() => {
	isLayoutReady.value = true;
});
</script>
