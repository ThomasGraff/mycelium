import { onMounted, onUnmounted } from 'vue'

export function useResizeObserver (selector) {
  const resizeObserverHandler = (entries) => {
    for (const entry of entries) {
      if (entry.target.clientHeight === 0) {
        return
      }
    }
  }

  let resizeObserver
  onMounted(() => {
    resizeObserver = new ResizeObserver(resizeObserverHandler)
    document.querySelectorAll(selector).forEach(el => {
      resizeObserver.observe(el)
    })
  })

  onUnmounted(() => {
    if (resizeObserver) {
      resizeObserver.disconnect()
    }
  })
}
