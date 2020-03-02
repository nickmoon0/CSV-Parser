<template>
	<div class="container-fluid">
		<!--<h1 v-if="error.statusCode === 404">Error (404): Page not found</h1>-->
		<h1>Error({{ error.statusCode }})</h1>
	</div>
</template>
<script>
export default {
	props: ['error']
}
</script>