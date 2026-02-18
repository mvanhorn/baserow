<template>
  <Expandable toggle-on-click>
    <template #header="{ expanded }">
      <div class="workflow-history__divider"></div>
      <div class="workflow-history__header">
        <Icon
          v-if="props.item.status === 'success'"
          icon="iconoir-check-circle"
          type="success"
        />
        <Icon v-else icon="iconoir-warning-circle" type="error" />
        <span class="workflow-history__header-title">
          {{ historyTitlePrefix }}{{ statusTitle }}
        </span>
        <span :title="completedDate" class="workflow-history__header-date">
          {{ humanCompletedDate }}
        </span>
        <Icon
          :icon="
            expanded ? 'iconoir-nav-arrow-down' : 'iconoir-nav-arrow-right'
          "
          type="secondary"
        />
      </div>
    </template>

    <template #default>
      <NodeHistory
        v-for="nodeHistory in props.item.node_histories"
        :key="nodeHistory.id"
        :node-history="nodeHistory"
        :node-depth="getNodeDepth(nodeHistory.node)"
      />
    </template>
  </Expandable>
</template>

<script setup>
import moment from '@baserow/modules/core/moment'
import { getUserTimeZone } from '@baserow/modules/core/utils/date'
import NodeHistory from '@baserow/modules/automation/components/workflow/sidePanels/NodeHistory.vue'

const app = useNuxtApp()

const props = defineProps({
  item: {
    type: Object,
    required: true,
  },
})

const statusTitle = computed(() => {
  switch (props.item.status) {
    case 'success':
      return app.$i18n.t('historySidePanel.statusSuccess')
    case 'error':
      return app.$i18n.t('historySidePanel.statusError')
    case 'started':
      return app.$i18n.t('historySidePanel.statusStarted')
    default:
      return app.$i18n.t('historySidePanel.statusDisabled')
  }
})

const completedDate = computed(() => {
  return moment
    .utc(props.item.completed_on)
    .tz(getUserTimeZone())
    .format('YYYY-MM-DD HH:mm:ss')
})

const humanCompletedDate = computed(() => {
  return moment.utc(props.item.completed_on).tz(getUserTimeZone()).fromNow()
})

const historyTitlePrefix = computed(() => {
  return props.item.is_test_run === true
    ? `[${app.$i18n.t('historySidePanel.testRun')}] `
    : ''
})

/**
 * Create a mapping of node IDs and their parent nodes IDs. The parent node ID
 * can be null if there is no parent.
 *
 * This is used to compute the node's depth.
 */
const nodeParentMap = computed(() => {
  const map = {}
  for (const nodeHistory of props.item.node_histories || []) {
    if (!(nodeHistory.node in map)) {
      map[nodeHistory.node] = nodeHistory.parent_node_id
    }
  }
  return map
})

/**
 * Return the depth of a given node ID.
 *
 * This is used to add the correct indentation to the node history.
 *
 * E.g. if a node has no parent, its depth is 0. If it has one parent,
 * its depth is 1, etc.
 */
const getNodeDepth = (nodeId) => {
  const parentId = nodeParentMap.value[nodeId]
  if (parentId == null) {
    return 0
  }
  return 1 + getNodeDepth(parentId)
}
</script>
