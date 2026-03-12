export default (client) => {
  return {
    fetchAll(pageId) {
      return client.get(`builder/page/${pageId}/elements/`)
    },
    create(
      pageId,
      elementType,
      referenceElement,
      position,
      configuration = null
    ) {
      const payload = {
        type: elementType,
        ...configuration,
      }

      if (referenceElement) {
        payload.reference_element_id = referenceElement.id
        payload.position = position
      }

      console.log('Creating element with payload', payload)

      return client.post(`builder/page/${pageId}/elements/`, payload)
    },
    update(elementId, values) {
      return client.patch(`builder/element/${elementId}/`, values)
    },
    delete(elementId) {
      return client.delete(`builder/element/${elementId}/`)
    },
    move(elementId, beforeId, parentElementId, placeInContainer) {
      return client.patch(`builder/element/${elementId}/move/`, {
        before_id: beforeId,
        parent_element_id: parentElementId,
        place_in_container: placeInContainer,
      })
    },
    duplicate(elementId) {
      return client.post(`builder/element/${elementId}/duplicate/`)
    },
  }
}
